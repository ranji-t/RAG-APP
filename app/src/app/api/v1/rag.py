# Third Party Imports
from fastapi import APIRouter, Request
from langchain_qdrant import QdrantVectorStore
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Internal Imports
from app.utils import DEFAULT_COLLECTIONS
from ...services.rag import get_custom_prompt, format_docs


#  Create the router
router = APIRouter()


@router.post("/ask")
async def ask_question(
    request: Request, question: str, collection_name: str = DEFAULT_COLLECTIONS
) -> dict[str, str]:
    # 1. Access state resources
    sync_client = request.app.state.qd_sync
    embedder = request.app.state.embedder
    llm = request.app.state.llm  # Assuming you added llm to state

    # 2. Setup the retriever
    vecstore = QdrantVectorStore(sync_client, collection_name, embedder)
    retriever = vecstore.as_retriever(search_kwargs={"k": 3})

    # 3. Define the Chain manually using LCEL
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | get_custom_prompt()
        | llm
        | StrOutputParser()
    )

    # 4. Execute Asynchronously
    answer = await rag_chain.ainvoke(question)

    # 5. Return the answer
    return {"answer": answer}
