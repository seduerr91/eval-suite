We're working on this:

Please prepare all the documents:

# DeepScribe AI Coding Assessment

At DeepScribe, we build AI products that generate clinical documentation for real patient encounters. These systems must reliably reflect what was said, capture critical information, and avoid hallucination. This assignment is your opportunity to show how you'd approach these challenges.

You have two options to choose from: 1) Evals Suite, 2) Choose your own adventure.

---

## Option 1: Evals Suite

**Context:** You’re given 100 SOAP notes, each paired with the source transcript and a ground-truth clinician-edited note. Your task is to build an evaluations suite that can evaluate notes and flag issues using scalable, statistically sound methods.

### Core Requirements

Your framework should identify problems such as:

- **Missing critical findings** - facts from the transcript that were omitted from the generated note.
- **Hallucinated or unsupported facts** - information in the note that isn’t grounded in the transcript.
- **Clinical accuracy issues** - medically incorrect or misleading statements

### Goals

At DeepScribe, we need to:

1. **Move fast** - We need to be able to quickly measure and incorporate the latest models and PR changes, without waiting days/weeks.
2. **Understand production quality** - It’s important for us to measure our note quality in the wild, so we can quickly detect any regressions or areas where notes may have lower quality.

### Evaluation Approaches

Consider the tradeoffs between different evaluation approaches:

1. **Reference-Based vs Non Reference-Based**: Some evals require ground truth datasets which can be expensive to curate, whereas other evals can run in an unsupervised fashion which are easier to scale.
2. **LLM-as-a-judge vs Deterministic Evals** - LLM-as-a-judge evals are very powerful, but they are also slower and costlier to run compared to deterministic metrics.

There are no wrong answers here - we’d encourage you to be creative and think outside the box. Be sure that the approach you take is focusing on the [Goals](https://www.notion.so/Goals-22d78d2a9ce3806fbee9cac2969b3307?pvs=21) outlined above. Also consider how you can measure the quality of the eval itself - e.g. how do you know if the eval is working?

### Deliverable

You need to have working code - implement a minimal eval suite and provide a write-up explaining your approach and justify how your metric(s) could be used to for goals 1 and 2. For bonus points (not required), you can add a dashboard summarizing your findings across all the notes.

Here are the different eval framework informations:
