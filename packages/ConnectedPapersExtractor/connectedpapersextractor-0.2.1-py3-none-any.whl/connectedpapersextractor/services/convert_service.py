from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from injector import inject
from injector import Injector

from .. import Article
from .. import ArticleFilterService
from .. import MainPartsExtractorService
from ..services.sumaries_combine import (
    SummariesCombineService, )
from ..services.summarizer import SummarizerService
from ..services.text_splitter import TextSplitterService  # noqa E501


class CovertService:
    @inject
    def __init__(
        self,
        text_splitter_service: TextSplitterService,
        main_parts_extractor: MainPartsExtractorService,
        summarizer_service: SummarizerService,
        article_filter_service: ArticleFilterService,
        summaries_combine_service: SummariesCombineService,
    ):
        self.summaries_combine_service = summaries_combine_service
        self.article_filter_service = article_filter_service
        self.summarizer_service = summarizer_service
        self.main_parts_extractor = main_parts_extractor
        self.text_splitter_service = text_splitter_service

    def add_summary(self, article: Article, metadata_path: Path) -> str:
        if article.text_summary is not None:
            return article.text_summary
        docs = self.text_splitter_service.split_text_to_documents(article)
        docs = self.main_parts_extractor.extract(docs)
        article.text_summary = self.summarizer_service.summarize(docs)
        summary_as_dict = asdict(article)
        metadata = json.loads(metadata_path.read_text())
        metadata[str(summary_as_dict.pop("file_path"))] = summary_as_dict
        metadata_path.write_text(json.dumps(metadata, indent=2))
        return article.text_summary


default_convert_service = Injector().get(CovertService)
