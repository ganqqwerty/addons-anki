# Anki AI Add-on Config

Anki AI is an addon that enriches your anki cards with the information from the artificial intelligence. This guide explains how to edit the configuration file for the Anki AI Add-on.

## Keys Explanation

- `apiKey`: Your OpenAI GPT API key. Get it from the OpenAI website.

- `emulate`: Set to "yes" to use fake responses for testing, "no" for real API requests.

- `prompts`: A list of prompts that the add-on can use. Each has:
  - `prompt`: This is the question or instruction that gets sent to the ChatGPT. 

    The `prompt` field can contain placeholders in the form of `{{{field_name}}}`. Each `field_name` should correspond to a field in your Anki notes. For example, if you have a field in your notes called "Word", you can use `{{{Word}}}` in your prompt.

    During processing, each `{{{field_name}}}` in the prompt will be replaced with the content of the corresponding field from the note that's currently being processed.

    For example, let's say you have a note with a "Word" field containing "apple", and a "Sentence" field containing "She ate an apple". If your prompt is "Explain the usage of the word {{{Word}}} in the following sentence: {{{Sentence}}}", it will be sent to the OpenAI API as "Explain the usage of the word apple in the following sentence: She ate an apple".

    You can include as many placeholders in your prompt as you want, as long as each corresponds to a field in your Anki notes. If a placeholder doesn't correspond to any field, you'll get an error message.

  - `targetField`: The field name where the API response will be stored.
  - `promptName`: A name for this prompt configuration to be shown in Anki UI.
