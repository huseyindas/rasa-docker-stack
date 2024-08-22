from phi.storage.assistant.postgres import PgAssistantStorage

from .consts import VECTOR_DB


combined_assistant_storage = PgAssistantStorage(
    db_url=VECTOR_DB,
    table_name="combined_assistant",
)