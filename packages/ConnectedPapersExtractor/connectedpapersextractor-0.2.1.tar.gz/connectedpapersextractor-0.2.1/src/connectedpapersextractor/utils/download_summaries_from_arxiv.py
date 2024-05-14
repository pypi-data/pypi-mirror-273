from __future__ import annotations

from pathlib import Path
from typing import Union

import arxiv

from .. import Article
from .. import Articles
from ..utils.download_summaries import download_summaries


def download_summaries_from_arxiv(
    search: arxiv.Search,
    dir_path: Union[str, Path] = Path("/"),
) -> Articles:
    dir_path = Path(dir_path)
    client = arxiv.Client()
    results = client.results(search)
    summaries = list(
        Article(
            file_path=dir_path.joinpath(
                article.entry_id.rpartition("/")[-1]
            ).with_suffix(".pdf"),
            download_link=article.pdf_url,
            year=article.published.year,
            title=article.title,
        )
        for article in results
    )
    download_summaries(summaries, dir_path)
    return summaries
