from __future__ import annotations

import json
import shutil
from os import PathLike
from typing import Optional

import arxiv

from . import ArticleFilterService
from . import Articles
from .Config import Config
from .utils.download_summaries_from_arxiv import (
    download_summaries_from_arxiv,
)
from .utils.get_existing_summaries import (
    check_for_existing_summaries,
)


def get_summaries_from_arxiv(
    search: arxiv.Search,
    pdf_output: Optional[PathLike[str]] = None,
    article_filter: Optional[ArticleFilterService] = None,
) -> Articles:
    article_filter, temp_pdf, summaries = check_for_existing_summaries(
        pdf_output, article_filter
    )
    if not summaries:
        summaries = download_summaries_from_arxiv(
            search,
            temp_pdf,
        )
    else:
        metadata = json.loads(
            temp_pdf.joinpath(Config.metadate_file_name).read_text()
        )
        for summary in summaries:
            for key, value in metadata[str(summary.file_path)].items():
                setattr(summary, key, value)
    if temp_pdf != pdf_output:
        shutil.rmtree(temp_pdf)
    return article_filter.filter(summaries)
