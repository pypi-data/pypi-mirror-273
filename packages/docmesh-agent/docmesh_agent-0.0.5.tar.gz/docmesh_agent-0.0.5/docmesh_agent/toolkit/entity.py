from langchain_core.tools import BaseToolkit

from docmesh_agent.tools.base import BaseAgentTool
from docmesh_agent.tools.entity import (
    FollowEntityTool,
    ListFollowsTool,
    ListPopularEntitiesTool,
)


class EntityToolkit(BaseToolkit):
    entity_name: str

    def get_tools(self) -> list[BaseAgentTool]:
        return [
            FollowEntityTool(entity_name=self.entity_name),
            ListFollowsTool(entity_name=self.entity_name),
            ListPopularEntitiesTool(entity_name=self.entity_name),
        ]
