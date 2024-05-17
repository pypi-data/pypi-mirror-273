from typing import Type, Optional
from langchain.pydantic_v1 import BaseModel, Field

from langchain.callbacks.manager import CallbackManagerForToolRun

from docmesh_core.db.neo import follow_entity, list_follows, list_popular_entities
from docmesh_agent.tools.base import BaseAgentTool, BaseAgentNoInputTool


class FollowEntityToolInput(BaseModel):
    name: str = Field(description="entity name")


class FollowEntityTool(BaseAgentTool):
    name: str = "follow_entity"
    description: str = "uesful when you need to follow an entity"
    args_schema: Optional[Type[BaseModel]] = FollowEntityToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        name = self._preporcess_input(name)
        follow_entity(self.entity_name, name)
        return f"\nSuccessfully follow entity {name}\n"


class ListFollowsTool(BaseAgentNoInputTool):
    name: str = "list_follows"
    description: str = "useful when you need to list all you follows"
    args_schema: Optional[Type[BaseModel]] = None
    handle_tool_error: bool = True

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        df = list_follows(entity_name=self.entity_name)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"


class ListPopularEntitiesToolInput(BaseModel):
    n: int = Field(description="number of entities")


class ListPopularEntitiesTool(BaseAgentTool):
    name: str = "list_popular_entities"
    description: str = "useful when you need to list popular entities"
    args_schema: Optional[Type[BaseModel]] = ListPopularEntitiesToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        n: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        n = self._preporcess_input(n)
        df = list_popular_entities(n=n)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"
