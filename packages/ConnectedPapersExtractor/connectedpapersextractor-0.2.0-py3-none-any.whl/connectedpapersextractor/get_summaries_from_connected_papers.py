from __future__ import annotations

import json
import shutil
from os import PathLike
from typing import Optional

from . import ArticleFilterService
from . import Articles
from .Config import Config
from .utils.download_summaries_from_connected_papers import (
    download_summaries_from_connected_papers,
)
from .utils.get_existing_summaries import (
    check_for_existing_summaries,
)


def get_summaries_from_connected_papers(
    connected_papers_url: str,
    pdf_output: Optional[PathLike[str]] = None,
    article_filter: Optional[ArticleFilterService] = None,
) -> Articles:
    article_filter, temp_pdf, summaries = check_for_existing_summaries(
        pdf_output, article_filter
    )
    if not summaries:
        summaries = download_summaries_from_connected_papers(
            connected_papers_url,
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
