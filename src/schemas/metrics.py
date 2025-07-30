from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

class SOAPStructureMetric(GEval):
    """Evaluates the structural integrity of a SOAP note."""
    def __init__(self, threshold: float = 0.8, **kwargs):
        params = {
            'name': "SOAP Structure Compliance",
            'criteria': """
            Evaluate if the clinical note follows proper SOAP format:
            1. Subjective: Patient-reported symptoms, chief complaint, history
            2. Objective: Vital signs, physical exam findings, lab results
            3. Assessment: Clinical impression, diagnoses
            4. Plan: Treatment plan, medications, follow-up instructions
            """,
            'evaluation_steps': [
                "Identify the presence of each SOAP section (Subjective, Objective, Assessment, Plan).",
                "Verify that appropriate content is present in each section (e.g., patient complaints in Subjective, exam findings in Objective).",
                "Assess the logical flow and consistency between the sections.",
                "Check for proper medical terminology usage within each section."
            ],
            'evaluation_params': [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.CONTEXT],
            'threshold': threshold
        }
        params.update(kwargs)
        super().__init__(**params)

class ClinicalSafetyMetric(GEval):
    """Evaluates the clinical safety of a generated note."""
    def __init__(self, threshold: float = 0.7, **kwargs):
        params = {
            'name': "Clinical Safety Assessment",
            'criteria': """
            Evaluate potential patient safety risks in the generated note:
            1. Medication errors (e.g., incorrect dosage, wrong medication).
            2. Omission of critical findings (e.g., urgent symptoms, abnormal vital signs).
            3. Diagnostic accuracy for high-risk conditions.
            4. Appropriateness and safety of the treatment plan.
            """,
            'evaluation_steps': [
                "Identify any medication mentions and check for potential errors (dosage, interactions).",
                "Check if any critical findings from the transcript are omitted in the note.",
                "Assess the diagnostic reasoning for accuracy and potential for harm.",
                "Evaluate the treatment recommendations for appropriateness and safety."
            ],
            'evaluation_params': [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.CONTEXT],
            'threshold': threshold
        }
        params.update(kwargs)
        super().__init__(**params)

class MedicalTerminologyMetric(GEval):
    """Evaluates the accuracy and appropriateness of medical terminology."""
    def __init__(self, threshold: float = 0.8, **kwargs):
        params = {
            'name': "Medical Terminology Accuracy",
            'criteria': """
            Evaluate the use of medical terminology in the clinical note for accuracy, context, and standard usage:
            1. Correctness: Are the terms spelled correctly and used in the proper medical context?
            2. Relevance: Is the terminology relevant to the patient's condition and findings?
            3. Clarity: Are abbreviations and jargon used appropriately and without ambiguity?
            """,
            'evaluation_steps': [
                "Scan the note for medical terms, abbreviations, and acronyms.",
                "Verify the spelling and contextual accuracy of each identified term.",
                "Assess whether the terminology is appropriate for the clinical scenario.",
                "Check for ambiguous or outdated abbreviations that could lead to misinterpretation."
            ],
            'evaluation_params': [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.CONTEXT],
            'threshold': threshold
        }
        params.update(kwargs)
        super().__init__(**params)

