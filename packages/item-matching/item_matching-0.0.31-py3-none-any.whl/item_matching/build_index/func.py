from pathlib import Path
import polars as pl
import re
from shutil import rmtree
from sklearn.feature_extraction.text import TfidfVectorizer

# Pre-compile the regular expression
regex_pattern = re.compile("[\(\[\<\"].*?[\)\]\>\"]")


class PipelineText:
    @staticmethod
    def clean_text(data: pl.DataFrame, col: str = 'item_name') -> pl.DataFrame:
        # Use the pre-compiled regex pattern
        def clean_func(x):
            return regex_pattern.sub("", x).lower().rstrip('.').strip()

        return data.with_columns(
            pl.col(col).map_elements(clean_func, return_dtype=pl.String)
            .alias(f'{col.lower()}_clean')
        )


def ngrams_func(string: str):
    ngrams = zip(*[string[i:] for i in range(3)])
    return [''.join(ngram) for ngram in ngrams]


def tfidf(lst_item: list, dim: int = 512):
    # Ensure the vectorizer is as efficient as possible
    vectorizer = TfidfVectorizer(analyzer=ngrams_func, max_features=dim)
    vectorizer.fit(lst_item)
    return vectorizer


def rm_all_folder(path: Path) -> None:
    # Use shutil.rmtree for more efficient directory removal
    rmtree(path)


def make_dir(folder_name: Path) -> None:
    # Remove redundant existence check
    folder_name.mkdir(parents=True, exist_ok=True)
