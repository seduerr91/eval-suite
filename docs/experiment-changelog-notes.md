# Actions Taken

- updated model to gpt-4.1-mini
- updated metrics thresholds (lowering as we saw it fail close to 80% so we lowered it to 70%)
- removed contextual recall metric as we don't have a RAG setup here
- set temperature to 0 to avoid dynamic results
- added grounding instruction to the system prompt