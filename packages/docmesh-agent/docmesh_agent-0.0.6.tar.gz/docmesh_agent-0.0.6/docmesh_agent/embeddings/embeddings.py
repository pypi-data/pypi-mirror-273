import os

from langchain_openai import OpenAIEmbeddings

from docmesh_core.db.neo import list_unembedded_papers, update_papers

NUM_DIMENSIONS = 1024


def query_embeddings(query: str) -> list[float]:
    # setup embeddings
    embeddings = OpenAIEmbeddings(
        base_url=os.getenv("OPENAI_EMBEDDING_API_BASE"),
        api_key=os.getenv("OPENAI_EMBEDDING_API_KEY"),
        model=os.getenv("OPENAI_EMBEDDING_MODEL"),
        dimensions=NUM_DIMENSIONS,
    )
    query_embedded = embeddings.embed_query(query)

    return query_embedded


def update_paper_embeddings() -> int:
    update_cnt = 0

    while True:
        unembedded_papers = list_unembedded_papers()

        if unembedded_papers.shape[0] == 0:
            break

        # setup embeddings
        embeddings = OpenAIEmbeddings(
            base_url=os.getenv("OPENAI_EMBEDDING_API_BASE"),
            api_key=os.getenv("OPENAI_EMBEDDING_API_KEY"),
            model=os.getenv("OPENAI_EMBEDDING_MODEL"),
            dimensions=NUM_DIMENSIONS,
        )

        texts = unembedded_papers.apply(
            lambda x: f"{x.title}\n{x.abstract}\n{x.summary}",
            axis=1,
        )
        texts_embedded = embeddings.embed_documents(texts.to_list())
        unembedded_papers["embedding_te3l"] = texts_embedded

        update_papers(unembedded_papers)
        update_cnt += unembedded_papers.shape[0]

    return update_cnt
