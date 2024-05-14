from __future__ import annotations

from .. import Config
from ..article import Articles
from ..services.convert_service import CovertService


def add_summaries(
    articles: Articles,
    convert_service: CovertService
) -> Articles:
    metadata_path = articles[0].file_path.parent.joinpath(
        Config.metadate_file_name)
    for article in articles:
        convert_service.add_summary(article, metadata_path)
    return articles
