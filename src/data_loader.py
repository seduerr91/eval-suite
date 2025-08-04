import logging
import os
from typing import List, Optional

import openai
import pandas as pd

from src.core.config import settings
from src.prompts.versions import get_prompt_messages
from src.schemas.models import ClinicalNote

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_note(transcript: str, prompt_version: Optional[str] = None) -> str:
    """Generates a structured clinical SOAP note using the configured LLM.
    
    Args:
        transcript: The transcript of the conversation between a healthcare provider and a patient.
        prompt_version: The version of the prompt to use. If None, the default version is used.
        
    Returns:
        The generated clinical note.
    """
    try:
        # Get the prompt messages for the specified version
        messages = get_prompt_messages(version=prompt_version, transcript=transcript)
        
        # Create the completion
        response = client.chat.completions.create(
            model=settings.GENERATION_LLM,
            temperature=0,
            messages=messages,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error generating note: {e}")
        return ""


def load_data(limit: int = None) -> List[ClinicalNote]:
    """Loads the dataset from the local data directory and returns a list of ClinicalNote objects."""
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dataset_path = os.path.join(project_root, "data", "test.json")

        if not os.path.exists(dataset_path):
            logging.error(
                f"Dataset file not found at {dataset_path}. Please run 'just setup-data' to download it."
            )
            return []

        df = pd.read_json(dataset_path)

        if limit:
            df = df.head(limit)

        notes = []
        for _, row in df.iterrows():
            # Use the prompt version from settings
            generated = generate_note(row["patient_convo"], prompt_version=settings.PROMPT_VERSION)
            notes.append(
                ClinicalNote(
                    transcript=row["patient_convo"],
                    note=row["soap_notes"],
                    generated_note=generated,
                )
            )
        return notes
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return []
