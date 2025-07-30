import logging
import pandas as pd
import os
from typing import List
import openai
from .schemas.models import ClinicalNote
from .core.config import settings

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_note(transcript: str) -> str:
    """Generates a structured clinical SOAP note using OpenAI's GPT-4-turbo."""
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a clinical documentation assistant trained to convert patient-provider conversations "
                        "into structured, accurate, and complete clinical notes. Use SOAP (Subjective, Objective, "
                        "Assessment, Plan) format. Only include medically relevant and clinically justifiable information. "
                        "Avoid speculation or unsupported claims. Maintain a concise professional tone. "
                        "Include appropriate clinical terminology where applicable."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "Here is a transcript of a conversation between a healthcare provider and a patient. "
                        "Please generate a structured clinical note in proper SOAP format based only on what is mentioned. "
                        "Ensure accurate summarization and preserve critical clinical findings. Transcript:\n\n"
                        f"{transcript}"
                    )
                }
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error generating note: {e}")
        return ""

def load_data(limit: int = None) -> List[ClinicalNote]:
    """Loads the dataset from the local data directory and returns a list of ClinicalNote objects."""
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dataset_path = os.path.join(project_root, 'data', 'test.json')

        if not os.path.exists(dataset_path):
            logging.error(f"Dataset file not found at {dataset_path}. Please run 'just setup-data' to download it.")
            return []

        df = pd.read_json(dataset_path)

        if limit:
            df = df.head(limit)

        notes = []
        for _, row in df.iterrows():
            generated = generate_note(row['patient_convo'])
            notes.append(
                ClinicalNote(
                    transcript=row['patient_convo'],
                    note=row['soap_notes'],
                    generated_note=generated
                )
            )
        return notes
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return []
