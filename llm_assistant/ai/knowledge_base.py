from phi.knowledge.website import WebsiteKnowledgeBase
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.knowledge.combined import CombinedKnowledgeBase
from phi.vectordb.pgvector import PgVector2
from phi.embedder.ollama import OllamaEmbedder
from ollama import Client

from .consts import (
    OLLAMA_HOST,
    OLLAMA_MODEL,
    VECTOR_DB,
    EMBEDDING,
    KNOWLEDGE_BASE_WEBSITES,
    KNOWLEDGE_BASE_PDF_URLS
)

website_urls = KNOWLEDGE_BASE_WEBSITES.split(";")
pdf_urls = KNOWLEDGE_BASE_PDF_URLS.split(";")

ollama_client = Client(host=OLLAMA_HOST)
ollama_client.pull(OLLAMA_MODEL)

ollama_embedder = OllamaEmbedder(
    model=OLLAMA_MODEL,
    host=OLLAMA_HOST,
    dimensions=EMBEDDING

)

website_knowledge_base = WebsiteKnowledgeBase(
    urls=website_urls,
    max_links=300,
    max_depth=50,
    vector_db=PgVector2(
        collection="website_documents",
        db_url=VECTOR_DB,
        embedder=ollama_embedder
    ),
)

pdf_knowledge_base = PDFUrlKnowledgeBase(
    urls=pdf_urls,
    vector_db=PgVector2(
        collection="pdf_documents",
        db_url=VECTOR_DB,
        embedder=ollama_embedder
    ),
)

knowledge_base = CombinedKnowledgeBase(
    sources=[
        website_knowledge_base,
        pdf_knowledge_base
    ],
    vector_db=PgVector2(
        collection="combined_documents",
        db_url=VECTOR_DB,
        embedder=ollama_embedder
    ),
)