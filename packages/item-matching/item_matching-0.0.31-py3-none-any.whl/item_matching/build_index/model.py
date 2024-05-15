import torch
from loguru import logger
import sys
from PIL import Image
from torch.nn import functional as F
from transformers import AutoProcessor, SiglipVisionModel, CLIPVisionModel

# Setup logger
logger.remove()
logger.add(sys.stdout, colorize=True, format='<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{function}</cyan> | <level>{message}</level>')

# Determine device
device = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'


class Model:
    def __init__(self):
        self.device = device
        self.model_cache = {}
        logger.info(f'[Model] Run on: {self.device}')

    def _load_model(self, model_id, model_class):
        if model_id not in self.model_cache:
            model = model_class.from_pretrained(model_id).to(self.device)
            self.model_cache[model_id] = model
        return self.model_cache[model_id]

    def get_img_model(self, model_id: str = 'google/siglip-base-patch16-224'):
        if model_id == 'google/siglip-base-patch16-224':
            img_model = self._load_model(model_id, SiglipVisionModel)
            img_processor = AutoProcessor.from_pretrained(model_id)
        else:
            img_model = self._load_model(model_id, CLIPVisionModel)
            img_processor = AutoProcessor.from_pretrained(model_id)
        logger.info(f'Image model: {model_id}')
        return img_model, img_processor

    def get_text_model(self, model_id: str = 'BAAI/bge-m3'):
        from FlagEmbedding import BGEM3FlagModel

        model = BGEM3FlagModel(model_id, use_fp16=True)
        return model

    @staticmethod
    def pp_sparse_tfidf(batch, vectorizer, col: str) -> dict:
        embeddings = vectorizer.transform(batch[col]).toarray()
        return {'tfidf_embed': embeddings}

    @staticmethod
    def pp_img(batch, model, processor, col: str) -> dict:
        images = [Image.open(i).convert('RGB') for i in batch[col]]
        inputs = processor(images=images, return_tensors='pt').to(device)
        with torch.inference_mode():
            outputs = model(**inputs)
        pooled_output = outputs.pooler_output
        embeddings = F.normalize(pooled_output, p=2, dim=1).cpu().numpy()
        return {'img_embed': embeddings}

    @staticmethod
    def pp_dense(batch, model, col: str) -> dict:
        embeddings = model.encode(
            batch[col],
            batch_size=512,
            max_length=80,
            return_dense=True,
            return_sparse=False,
            return_colbert_vecs=False
        )['dense_vecs']
        embeddings = F.normalize(torch.tensor(embeddings), p=2, dim=1).cpu().numpy()
        return {'dense_embed': embeddings}
