import os
from deepeval import evaluate
from deepeval.metrics import HallucinationMetric, ContextualRecallMetric, GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from typing import List
from .schemas.models import ClinicalNote, EvaluationResult
from .schemas.metrics import SOAPStructureMetric, ClinicalSafetyMetric, MedicalTerminologyMetric
import json

def run_evaluation(notes: List[ClinicalNote]) -> List[EvaluationResult]:
    """Runs the DeepEval evaluation on a list of clinical notes."""

    # Create a list of test cases from the clinical notes
    test_cases = [
        LLMTestCase(
            input=note.transcript,
            actual_output=note.generated_note,
            expected_output=note.ground_truth_note,
            context=[note.ground_truth_note],
            retrieval_context=[note.transcript]
        )
        for note in notes
    ]

    # Define the metrics to run
    metrics_to_run = [
        HallucinationMetric(threshold=0.3),
        ContextualRecallMetric(threshold=0.8),
        GEval(
            name="Clinical Accuracy",
            criteria="Evaluate the clinical accuracy of the generated note. It should be medically sound and not contain misleading information.",
            evaluation_steps=[
                "Check for any medically incorrect statements.",
                "Verify that medical terminology is appropriate.",
                "Assess if the assessment and plan are clinically reasonable."
            ],
            evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.CONTEXT]
        ),
        SOAPStructureMetric(threshold=0.9),
        ClinicalSafetyMetric(threshold=0.7),
        MedicalTerminologyMetric(threshold=0.8)
    ]

    # Run the evaluation in parallel
    evaluation_output = evaluate(test_cases=test_cases, metrics=metrics_to_run)
    if not evaluation_output.test_results:
        raise ValueError("Evaluation failed to return results.")

    # Process the results
    results = []
    for i, test_result in enumerate(evaluation_output.test_results):
        note = notes[i]
        # Add a check to handle cases where the evaluation returns None.
        if not test_result.metrics_data:
            print(f"Warning: Evaluation failed for note {i}, skipping.")
            continue
        scores_dict = {m.name: m.score for m in test_result.metrics_data}

        hallucination_score = scores_dict.get("Hallucination", 0.0)
        recall_score = scores_dict.get("Contextual Recall", 0.0)
        accuracy_score = scores_dict.get("Clinical Accuracy [GEval]", 0.0)
        soap_score = scores_dict.get("SOAP Structure Compliance [GEval]", 0.0)
        safety_score = scores_dict.get("Clinical Safety Assessment [GEval]", 0.0)
        terminology_score = scores_dict.get("Medical Terminology Accuracy [GEval]", 0.0)

        overall_score = sum([
            hallucination_score, recall_score, accuracy_score,
            soap_score, safety_score, terminology_score
        ]) / 6

        results.append(
            EvaluationResult(
                note=note,
                hallucination_score=hallucination_score,
                missing_info_score=recall_score,
                clinical_accuracy_score=accuracy_score,
                soap_structure_score=soap_score,
                clinical_safety_score=safety_score,
                medical_terminology_score=terminology_score,
                overall_score=overall_score
            )
        )

    return results
