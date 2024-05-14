from __future__ import annotations

from typing import Optional

from .article import Articles
from .services.convert_service import CovertService
from .services.convert_service import default_convert_service
from .utils.summarize_documents import (
    add_summaries,
)

Default = None


def create_related_work(
    summaries: Articles,
    convert_service: Optional[CovertService] = Default,
) -> str:
    if not summaries:
        raise ValueError("Summaries must be provided")
    if convert_service is None:
        convert_service = default_convert_service
    articles_with_summaries = add_summaries(summaries, convert_service)
    summaries_combine_service = convert_service.summaries_combine_service
    return summaries_combine_service.combine(articles_with_summaries)
