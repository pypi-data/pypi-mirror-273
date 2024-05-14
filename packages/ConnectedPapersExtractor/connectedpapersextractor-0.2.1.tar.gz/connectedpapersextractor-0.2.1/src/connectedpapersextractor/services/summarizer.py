from __future__ import annotations

from injector import inject
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI

from ..article import Documents


@inject
class SummarizerService:
    def __init__(self, model_name="gpt-3.5-turbo", temperature=.4):
        self.temperature = temperature
        self.model_name = model_name

    def summarize(self, docs: Documents) -> str:
        llm = ChatOpenAI(
            temperature=self.temperature,
            model_name=self.model_name
        )
        chain = load_summarize_chain(llm)
        return chain.run(docs)
