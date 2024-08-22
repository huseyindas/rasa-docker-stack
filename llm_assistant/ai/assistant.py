import os
from textwrap import dedent
from typing import Optional

from phi.assistant import Assistant
from phi.llm.ollama import Ollama

from .storage import combined_assistant_storage
from .knowledge_base import knowledge_base
from .consts import OLLAMA_HOST, OLLAMA_MODEL


def get_assistant(
    run_id: Optional[str] = None,
    user_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Assistant:
    """Get an Assistant with a combined knowledge base."""

    return Assistant(
        run_id=run_id,
        user_id=user_id,
        llm=Ollama(
            model=OLLAMA_MODEL,
            host=OLLAMA_HOST,
        ),
        storage=combined_assistant_storage,
        knowledge_base=knowledge_base,
        description="You are a helpful assistant named 'sba' designed to answer questions about PDF and website contents.",
        instructions=[
            "Keep your answers under 2 sentences.",
            "You are an information assistant and are here to answer user questions about the content on this website and the uploaded PDF files.", 
            "You should provide clear and accurate information to the user when giving your answers.",
            "If you do not have the knowledge to directly answer the question asked, you should instead guide or direct them to additional sources.",
            "Indicate to the user where you are quoting from and which file you are using.",
            "Also, if the user asks a question about membership, collect their name, phone, email, organization information and write it to the txt file using the tool I gave you."
        ],
        extra_instructions=[
            "Keep your answers under 2 sentences.",
        ],
        add_references_to_prompt=True,
    )