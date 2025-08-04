from pydantic import BaseModel, Field
from typing import Optional

class ClinicalNote(BaseModel):
    transcript: str = Field(
        ..., description="The source transcript of the patient encounter."
    )
    ground_truth_note: str = Field(
        ..., alias="note", description="The ground-truth, clinician-edited SOAP note."
    )
    generated_note: str = Field(..., description="The AI-generated SOAP note.")


class EvaluationResult(BaseModel):
    note: ClinicalNote
    hallucination_score: float
    missing_info_score: Optional[float] = None
    clinical_accuracy_score: float
    soap_structure_score: float
    clinical_safety_score: float
    medical_terminology_score: float
    overall_score: float
