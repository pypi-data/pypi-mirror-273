from __future__ import annotations

from injector import inject
from langchain_community.document_loaders import PyPDFLoader

from .. import Article
from ..article import Documents


@inject
class TextSplitterService:
    def __init__(self):
        pass

    def split_text_to_documents(self, summary: Article) -> Documents:
        loader = PyPDFLoader(str(summary.file_path))
        documents = loader.load()
        for document in documents:
            document.metadata["source"] = str(summary.file_path)
        return documents
