# Third Party Imports
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


async def chunk_docs(page_content: str, metadata_source: str) -> list[Document]:
    """Split the documents into chunks."""
    # 1. Convert to Documents
    doc = Document(page_content=page_content, metadata={"source": metadata_source})

    # 2. Document chunks
    doc_splits = RecursiveCharacterTextSplitter(
        chunk_size=1_000, chunk_overlap=100, add_start_index=True
    ).split_documents([doc])

    # 3. Return document chunks
    return doc_splits
