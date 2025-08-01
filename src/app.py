import json

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Clinical AI Evaluation Dashboard", layout="wide")

st.title("Clinical AI Evaluation Dashboard")


@st.cache_data
def load_results():
    try:
        with open("data/evaluation_results.json", "r") as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except FileNotFoundError:
        return None


df = load_results()

if df is not None:
    tab1, tab2 = st.tabs(["📊 Aggregate Analysis", "📄 Individual Note Review"])

    with tab1:
        st.header("Overall Performance Metrics")

        # Calculate all average scores
        avg_scores = {
            "Overall Score": df["overall_score"].mean(),
            "Patient Safety": df["clinical_safety_score"].mean(),
            "SOAP Compliance": df["soap_structure_score"].mean(),
            "Clinical Accuracy": df["clinical_accuracy_score"].mean(),
            "Terminology Accuracy": df["medical_terminology_score"].mean(),
            "Hallucination": df["hallucination_score"].mean(),
            "Missing Info": df["missing_info_score"].mean(),
        }

        metric_tooltips = {
            "Overall Score": "A weighted average of all other scores, providing a single measure of the model's performance.",
            "Patient Safety": "Assesses the clinical safety of the generated note. It penalizes any information that could lead to patient harm. Scores range from 0 to 1, where 1 is the best.",
            "SOAP Compliance": "Checks if the note follows the Subjective, Objective, Assessment, and Plan (SOAP) format. This is a binary score (1 for compliant, 0 for non-compliant).",
            "Clinical Accuracy": "Measures how accurately the generated note reflects the information in the transcript. Scores range from 0 to 1, where 1 is the best.",
            "Terminology Accuracy": "Evaluates the correct use of medical terminology in the generated note. Scores range from 0 to 1, where 1 is the best.",
            "Hallucination Score": "Detects any information in the generated note that was not mentioned in the transcript. Scores range from 0 to 1, where 0 is the best.",
            "Missing Info Score": "Identifies any important information from the transcript that is missing in the generated note. Scores range from 0 to 1, where 0 is the best.",
        }

        # Display metrics in two rows
        cols1 = st.columns(4)
        cols2 = st.columns(3)

        cols1[0].metric(
            "Overall Score",
            f"{avg_scores['Overall Score']:.2f}",
            help=metric_tooltips["Overall Score"],
        )
        cols1[1].metric(
            "Patient Safety",
            f"{avg_scores['Patient Safety']:.2f}",
            help=metric_tooltips["Patient Safety"],
        )
        cols1[2].metric(
            "SOAP Compliance",
            f"{avg_scores['SOAP Compliance']:.1%}",
            help=metric_tooltips["SOAP Compliance"],
        )
        cols1[3].metric(
            "Clinical Accuracy",
            f"{avg_scores['Clinical Accuracy']:.2f}",
            help=metric_tooltips["Clinical Accuracy"],
        )
        cols2[0].metric(
            "Terminology Accuracy",
            f"{avg_scores['Terminology Accuracy']:.2f}",
            help=metric_tooltips["Terminology Accuracy"],
        )
        cols2[1].metric(
            "Hallucination Score",
            f"{avg_scores['Hallucination']:.2f}",
            help=metric_tooltips["Hallucination Score"],
        )
        cols2[2].metric(
            "Missing Info Score",
            f"{avg_scores['Missing Info']:.2f}",
            help=metric_tooltips["Missing Info Score"],
        )

        st.header("Metric Scores Overview")
        # Create a bar chart for average scores
        metric_names = list(avg_scores.keys())[
            1:
        ]  # Exclude overall score from chart for better scale
        metric_values = [
            list(avg_scores.values())[i] for i in range(1, len(avg_scores))
        ]

        fig = go.Figure(
            data=[
                go.Bar(
                    x=metric_names,
                    y=metric_values,
                    text=[f"{v:.2f}" for v in metric_values],
                    textposition="auto",
                )
            ]
        )
        fig.update_layout(
            title_text="Average Scores by Metric",
            xaxis_title="Metric",
            yaxis_title="Average Score",
            yaxis=dict(range=[0, 1]),
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("Explore Individual Notes")
        selected_index = st.selectbox(
            "Select a note to review:", df.index, key="note_selector"
        )

        if selected_index is not None:
            note_data = df.loc[selected_index]

            st.subheader("Clinical Scores")
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.metric(
                "Safety",
                f"{note_data['clinical_safety_score']:.2f}",
                help=metric_tooltips["Patient Safety"],
            )
            col2.metric(
                "SOAP",
                f"{note_data['soap_structure_score']:.2f}",
                help=metric_tooltips["SOAP Compliance"],
            )
            col3.metric(
                "Accuracy",
                f"{note_data['clinical_accuracy_score']:.2f}",
                help=metric_tooltips["Clinical Accuracy"],
            )
            col4.metric(
                "Terminology",
                f"{note_data['medical_terminology_score']:.2f}",
                help=metric_tooltips["Terminology Accuracy"],
            )
            col5.metric(
                "Hallucination",
                f"{note_data['hallucination_score']:.2f}",
                help=metric_tooltips["Hallucination Score"],
            )
            col6.metric(
                "Missing Info",
                f"{note_data['missing_info_score']:.2f}",
                help=metric_tooltips["Missing Info Score"],
            )

            st.subheader("Note Details")
            note_details = note_data["note"]

            with st.expander("Source Transcript"):
                st.text(note_details["transcript"])
            with st.expander("Ground Truth Note"):
                st.text(note_details["ground_truth_note"])
            with st.expander("Generated Note"):
                st.text(note_details["generated_note"])
else:
    st.warning(
        "Evaluation results not found. Please run the evaluation first using `just run`."
    )
