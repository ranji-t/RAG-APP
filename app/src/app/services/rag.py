# Third Party Imports
from langchain_core.prompts import ChatPromptTemplate


def get_custom_prompt():
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
    return custom_prompt


# Helper to format docs into a single string for the prompt
def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)
