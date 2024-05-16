import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from typing import Type, Optional
from langchain.pydantic_v1 import BaseModel, Field

from datetime import datetime
from langchain.callbacks.manager import CallbackManagerForToolRun

from docmesh_core.db.neo import get_latest_citegraph
from docmesh_core.utils.graph_utils import find_max_degree_nodes
from docmesh_agent.tools.base import BaseAgentTool


class CiteGraphToolInput(BaseModel):
    n: str = Field(description="number of papers")


class CiteGraphTool(BaseAgentTool):
    name: str = "cite graph generation tool"
    description: str = (
        "useful when you need to generate a cite graph from papers, "
        "return a gml format of cite graph for a given number."
    )
    args_schema: Type[BaseModel] = CiteGraphToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        n: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        try:
            n = int(n)
        except Exception:
            self._raise_tool_error(
                "Input argument `n` should be an integer, please check your inputt. "
                "You can directly call this function to generate cite graph for latest papers. "
                "Pay attention that you MUST ONLY input the number, like 1, 3, 5.\n"
            )

        # fetch latest citegraph
        df = get_latest_citegraph(entity_name=self.entity_name, n=n)

        G = nx.Graph()
        G.add_edges_from(zip(df["p1_paper_id"], df["p2_paper_id"]))

        # generate gml file
        gml_file = f"{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.gml"
        nx.write_gml(G, gml_file)

        return f"\nCite graph is generate as gml file {gml_file}.\n"


class CiteGraphVisualizeToolInput(BaseModel):
    gml_file: str = Field(description="gml file to visualize")


class CiteGraphVisualizeTool(BaseAgentTool):
    name: str = "cite graph visualize tool"
    description: str = (
        "useful when you need to visualize a cite graph, return a png file for a given gml format cite graph. "
    )
    args_schema: Type[BaseModel] = CiteGraphVisualizeToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        gml_file: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        if not os.path.exists(gml_file):
            self._raise_tool_error(f"Cannot find gml file {gml_file}, please check your provided file name.")

        # read gml file
        G = nx.read_gml(gml_file)
        # draw networkx
        nx.draw_networkx(G, width=0.1, with_labels=False, node_size=1)

        # generate png file
        png_file = f"{os.path.splitext(gml_file)[0]}.png"
        # save png file
        plt.savefig(png_file, dpi=200)

        return f"\nCite graph visualized plot is saved to {png_file}.\n"


class PopularPaperToolInput(BaseModel):
    gml_file: str = Field(description="gml file to analyze")


class PopularPaperTool(BaseAgentTool):
    name: str = "popluar paper analysis tool"
    description: str = (
        "useful when you need to find out the popluar paper, "
        "return a list of paper ids for a given gml format cite graph. "
    )
    args_schema: Type[BaseModel] = PopularPaperToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        gml_file: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        if not os.path.exists(gml_file):
            self._raise_tool_error(f"Cannot find gml file {gml_file}, please check your provided file name.")

        # read gml file
        G = nx.read_gml(gml_file)
        # convert G to adj_mat
        A = nx.adjacency_matrix(G, G.nodes)
        # find max degree nodes
        node_indices = find_max_degree_nodes(A)
        nodes = np.array(G.nodes)[node_indices]
        nodes_repr = ", ".join(nodes)

        return f"\n{nodes_repr}\n"
