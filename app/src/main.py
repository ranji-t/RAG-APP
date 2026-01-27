# Standard Imports
import uuid

# Third Party Imports
from fastapi import FastAPI
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Internal Imports
from app.utils import DEFAULT_COLLECTIONS
from app.core import lifespan
from app.services import CollectionsService, chunk_docs


# The apps and services
app = FastAPI(lifespan=lifespan, debug=True, title="The RAG backend", version="0.0.1")


@app.get("/")
async def home() -> dict[str, str]:
    """Root endpoint verifying the application is running."""
    return {"message": "Welcome to the RAG backend"}


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"message": "OK"}


@app.get("/embed_query")
async def embed_query(text: str) -> dict[str, list[float]]:
    """Embed a single query string using the configured embedding model."""
    # 1. Gater resources
    embedder = app.state.embedder

    # 2. Get Embeddings of the query
    results = await embedder.aembed_query(text)

    # 3. Return
    return {"embedding": results}


@app.post("/embed")
async def embed(texts: list[str]) -> dict[str, list[list[float]]]:
    """Embed a list of text strings using the configured embedding model."""
    # 1. Gater resources
    embedder = app.state.embedder

    # 2. Get Embeddings of the texts
    results = await embedder.aembed_documents(texts)

    # 3. Return the Embeddings
    return {"embeddings": results}


@app.get("/collections")
async def collections() -> dict[str, list[str]]:
    """Retrieve the list of available collections in Qdrant."""
    # 1. Gater resources
    qd_client = app.state.qd_async

    # 2. Return the collections list
    return {
        "collections": [
            col.name
            for col in (
                await CollectionsService.list_collections(qd_client)
            ).collections
        ]
    }


@app.post("/collections")
async def create_collection(name: str | None = DEFAULT_COLLECTIONS):
    """Create a new collection in Qdrant if it does not already exist."""
    # 1. Gater resources
    qd_client = app.state.qd_async

    # 2. Create the collection
    collection_name = name if name is not None else DEFAULT_COLLECTIONS
    message = await CollectionsService.create_collection(qd_client, collection_name)

    # 3. Return the message
    return {"message": message}


@app.delete("/collections")
async def flush_collection(collection_name: str = DEFAULT_COLLECTIONS):
    """Delete a specific collection from Qdrant."""
    # 1. Gater resources
    qd_client = app.state.qd_async

    # 2. Delete the collection
    message = await CollectionsService.delete_collection(qd_client, collection_name)

    # 3. Return the message
    return {"message": message}


@app.post("/add_docs")
async def add_docs(
    page_content: str, metadata_source: str, collection_name: str = DEFAULT_COLLECTIONS
):
    """Add documents to the Qdrant vector store after chunking and embedding them."""
    # 1. Gater resources
    qd_client_sync = app.state.qd_sync
    embedder = app.state.embedder

    # 2. Split the docs
    doc_splits = await chunk_docs(
        page_content=page_content, metadata_source=metadata_source
    )

    # 3. Get IDs
    ids = [uuid.uuid5(uuid.NAMESPACE_DNS, f"{doc.metadata}") for doc in doc_splits]

    # 4. Create the vector store
    vecstore = QdrantVectorStore(qd_client_sync, collection_name, embedder)

    # 5. Add the docs to images
    await vecstore.aadd_documents(doc_splits, ids=ids)

    # 6. Return the message with number of docs added
    return {"message": f"Added {len(doc_splits)} documents to {collection_name}"}


@app.post("/query")
async def query(query: str, k: int = 5, collection_name: str = DEFAULT_COLLECTIONS):
    """Search for similar documents in the Qdrant vector store based on the query."""
    # 1. Gater resources
    qd_client_sync = app.state.qd_sync
    embedder = app.state.embedder

    # 2. Create the vector store
    vecstore = QdrantVectorStore(qd_client_sync, collection_name, embedder)

    # 3. Get results
    results = await vecstore.asimilarity_search(query, k=k)

    # 4. Return the results
    return {"results": results}


# 1. Custom System Message: Setting the 'Ground Rules'
system_prompt = (
    "You are a technical assistant for a RAG application. "
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, just say that you don't know, don't try to make up an answer. "
    "Keep the answer concise and professional and related to context. If the answer is not in the context, just say that you don't know."
    "Give references to the context if the answer is in the context."
    "\n\n"
    "Context:\n{context}"
)
custom_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{question}"),
    ]
)


# Helper to format docs into a single string for the prompt
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


@app.post("/ask")
async def ask_question(question: str, collection_name: str = DEFAULT_COLLECTIONS):
    # 1. Access state resources
    sync_client = app.state.qd_sync
    embedder = app.state.embedder
    llm = app.state.llm  # Assuming you added llm to state

    # 2. Setup the retriever
    vecstore = QdrantVectorStore(sync_client, collection_name, embedder)
    retriever = vecstore.as_retriever(search_kwargs={"k": 3})

    # 3. Define the Chain manually using LCEL
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_prompt
        | llm
        | StrOutputParser()
    )

    # 4. Execute Asynchronously
    answer = await rag_chain.ainvoke(question)

    return {"answer": answer}
