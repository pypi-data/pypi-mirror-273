from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Optional

from injector import Injector

from .. import Article
from .. import ArticleFilterService
from .. import Articles
from ..Config import Config


def check_for_existing_summaries(
    pdf_output: Optional[PathLike[str]] = None,
    article_filter: Optional[ArticleFilterService] = None,
) -> tuple[ArticleFilterService, Path, Articles]:
    if article_filter is None:
        article_filter = Injector().get(ArticleFilterService)
    temp_pdf = Path(
        pdf_output or Path(__file__).parent.joinpath(Config.temp_pdf_path)
    )
    temp_pdf.mkdir(exist_ok=True, parents=True)
    summaries = list(
        filter(
            lambda summary: summary.is_valid(),
            (Article(pdf_file) for pdf_file in temp_pdf.glob("*.pdf")),
        )
    )
    return article_filter, temp_pdf, summaries
