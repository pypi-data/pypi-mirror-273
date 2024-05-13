import os

from typing import Type, Optional
from langchain.pydantic_v1 import BaseModel, Field

from datetime import datetime
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_openai import OpenAIEmbeddings

from docmesh.db.neo import (
    list_unread_follows_papers,
    list_unread_influential_papers,
    list_unread_similar_papers,
    list_unread_semantic_papers,
)
from docmesh_agent.tools.base import BaseAgentTool


class UnreadFollowsToolInput(BaseModel):
    n: str = Field(description="number of papers")


class UnreadFollowsTool(BaseAgentTool):
    name: str = "recommend_papers_from_follows"
    description: str = "useful when you need to get some recommanded papers from follows"
    args_schema: Optional[Type[BaseModel]] = UnreadFollowsToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        n: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        n = self._preporcess_input(n)
        try:
            n = int(n)
        except Exception:
            self._raise_tool_error(
                "Input argument `n` should be an integer, please check your inputt. "
                "Pay attention that you MUST ONLY input the number, like 1, 3, 5.\n"
            )

        df = list_unread_follows_papers(entity_name=self.entity_name, n=n)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"


class UnreadInfluentialToolInput(BaseModel):
    date_time: str = Field(description="publication date time of papers")


class UnreadInfluentialTool(BaseAgentTool):
    name: str = "recommend_latest_influential_papers"
    description: str = "useful when you need to get some influential papers from a given date"
    args_schema: Optional[Type[BaseModel]] = UnreadInfluentialToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        date_time: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        date_time = self._preporcess_input(date_time)
        try:
            datetime.strptime(date_time, "%Y-%m-%d")
        except Exception:
            self._raise_tool_error(
                "Input argument `date_time` should be written in format `YYYY-MM-DD`, "
                "please check your input, valid input can be 1995-03-01, 2024-01-01.\n"
            )

        df = list_unread_influential_papers(entity_name=self.entity_name, date_time=date_time)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"


class UnreadSimilarToolInput(BaseModel):
    paper_id: str = Field(description="paper id")


class UnreadSimilarTool(BaseAgentTool):
    name: str = "recommend_similar_papers"
    description: str = "useful when you need to get some similar papers from provided paper id"
    args_schema: Optional[Type[BaseModel]] = UnreadSimilarToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper_id = self._preporcess_input(paper_id)
        df = list_unread_similar_papers(
            entity_name=self.entity_name,
            paper_id=paper_id,
            n=10,
        )
        # keep score over 0.5 and drop the column
        df = df[df["score"] > 0.5].drop(columns="score")
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"


class UnreadSemanticToolInput(BaseModel):
    query: str = Field(description="search query")


class UnreadSemanticTool(BaseAgentTool):
    name: str = "recommend_queried_papers"
    description: str = "useful when you need to get some papers from a query"
    args_schema: Optional[Type[BaseModel]] = UnreadSemanticToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        query = self._preporcess_input(query)

        # setup embedding
        embedding = OpenAIEmbeddings(
            base_url=os.getenv("OPENAI_EMBEDDING_API_BASE"),
            api_key=os.getenv("OPENAI_EMBEDDING_API_KEY"),
            model=os.getenv("OPENAI_EMBEDDING_MODEL"),
            dimensions=1024,
        )
        query_embedded = embedding.embed_query(query)

        df = list_unread_semantic_papers(
            entity_name=self.entity_name,
            semantic_embedding=query_embedded,
            n=10,
        )
        # keep score over 0.5 and drop the column
        df = df[df["score"] > 0.5].drop(columns="score")
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"
