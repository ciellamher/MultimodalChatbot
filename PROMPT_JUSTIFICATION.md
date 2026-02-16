# Prompt Justification

## 1. Objective & Constraints
The goal is to create a multimodal assistant that acts as a strict dictionary. 
- **Input:** Single words or images.
- **Output:** Strict JSON format containing definitions, parts of speech, and synonyms (for words) or labels and descriptions (for images).
- **Constraints:** No conversational filler ("Here is your definition"), strictly factual, and must refuse unsafe content.

## 2. Prompt Design
**Role:** "You are a precise, neutral dictionary assistant."
**Instructions:** - For words: Return `word`, `part_of_speech`, `definition`, `examples`, `synonyms`.
- For images: Return `label`, `description`, `meaning`.
**Style:** Academic, concise, objective.

**Few-shot Example (Word):**
User: "Apple"
Assistant: {
  "word": "apple",
  "part_of_speech": "noun",
  "definition": "The round fruit of a tree of the rose family.",
  "examples": ["I ate a red apple."],
  "synonyms": ["pome"]
}

## 3. Parameters
- **Temperature:** 0.2. We need high consistency and factual accuracy. Creativity is not required for a dictionary.
- **Top_p:** 1.0. Standard sampling to ensure grammatical correctness.

## 4. Risk & Mitigation
- **Ambiguity:** If a word has multiple meanings (e.g., "Bank"), the prompt instructs the model to "Prefer the most common sense" or return the primary definition.
- **Hallucination:** By setting a low temperature (0.2) and demanding a strict JSON schema, we reduce the risk of the model inventing words.