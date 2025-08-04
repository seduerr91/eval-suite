"""
Prompt versions for generating clinical SOAP notes.
This module contains different versions of prompts that can be used for generating
clinical SOAP notes from patient-provider conversations.
"""

from typing import Dict, List, Optional


class PromptVersion:
    """A class representing a prompt version with its messages."""

    def __init__(self, version: str, messages: List[Dict[str, str]]):
        """
        Initialize a prompt version.

        Args:
            version: The version identifier.
            messages: The list of messages for this prompt version.
        """
        self.version = version
        self.messages = messages

    def get_messages(self, transcript: str) -> List[Dict[str, str]]:
        """
        Get the messages for this prompt version with the transcript inserted.

        Args:
            transcript: The transcript to insert into the prompt.

        Returns:
            The list of messages with the transcript inserted.
        """
        # Create a deep copy of the messages to avoid modifying the original
        messages_copy = []
        for message in self.messages:
            message_copy = message.copy()
            if "{transcript}" in message_copy.get("content", ""):
                message_copy["content"] = message_copy["content"].format(
                    transcript=transcript
                )
            messages_copy.append(message_copy)
        return messages_copy


# Default prompt version (v1)
DEFAULT_VERSION = "v1"

# Define the prompt versions
PROMPT_VERSIONS = {
    "v1": PromptVersion(
        version="v1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a clinical documentation assistant trained to convert patient-provider conversations "
                    "into structured, accurate, and complete clinical notes. Use SOAP (Subjective, Objective, "
                    "Assessment, Plan) format. Only include medically relevant and clinically justifiable information. "
                    "Avoid speculation or unsupported claims. Maintain a concise professional tone. "
                    "Include appropriate clinical terminology where applicable."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Here is a transcript of a conversation between a healthcare provider and a patient. "
                    "Please generate a structured clinical note in proper SOAP format based only on what is mentioned. "
                    "Ensure accurate summarization and preserve critical clinical findings. Transcript:\n\n"
                    "{transcript}"
                ),
            },
        ],
    ),
    "v2": PromptVersion(
        version="v2",
        messages=[
            {
                "role": "system",
                "content": (
                    """You are an expert medical scribe trained to convert patient-provider conversations
                    into comprehensive clinical SOAP notes. Focus on accuracy, completeness, and clinical relevance.
                    Use proper medical terminology and maintain a professional tone.
                    Ground your results in the transcript.
                    """
                ),
            },
            {
                "role": "user",
                "content": (
                    "Convert the following healthcare conversation into a detailed SOAP note. "
                    "Ensure all sections (Subjective, Objective, Assessment, Plan) are complete and accurate. "
                    "Only include information explicitly mentioned in the transcript. Transcript:\n\n"
                    "{transcript}"
                ),
            },
        ],
    ),
}


def get_prompt_messages(
    version: Optional[str] = None, transcript: str = ""
) -> List[Dict[str, str]]:
    """
    Get the prompt messages for the specified version.

    Args:
        version: The version to get. If None, the default version is used.
        transcript: The transcript to insert into the prompt.

    Returns:
        The list of messages for the specified version with the transcript inserted.
    """
    version = version or DEFAULT_VERSION
    if version not in PROMPT_VERSIONS:
        raise ValueError(f"Unknown prompt version: {version}")

    return PROMPT_VERSIONS[version].get_messages(transcript)
