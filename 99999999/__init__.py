import json
from pprint import pprint
import inspect

import requests
from aqt import mw
from aqt.utils import tooltip
from aqt.qt import QAction
from anki.hooks import addHook
from aqt.utils import showWarning


# Function to send a prompt to the ChatGPT API

def send_prompt(prompt):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(api_url, headers=headers, json=data)

    print("ChatGPT addon: result from chatgpt:")
    pprint(response.json())

    if response.status_code == 200:
        result = response.json()
        completion = result["choices"][0]["message"]["content"].strip()
        return completion
    else:
        error_message = response.json().get("error", {}).get(
            "message") or "An error occurred while making the API call."
        raise Exception(error_message)


# Function to process the note and generate the result
def process_note(note):
    print("ChatGPT addon: note to process ")
    pprint(inspect.getmembers(note))

    # Check if the target field and source fields exist in the note
    target_field = "ChatGPT Output"
    source_fields = ["Sentence", "Word"]

    if target_field not in note:
        return showWarning(f"Target field '{target_field}' is missing in the note.")

    for field in source_fields:
        if field not in note:
            return showWarning(f"Source field '{field}' is missing in the note.")

    # Get the content from the fields and assign them to variables
    sentence = note["Sentence"]
    target_word = note["Word"]

    # Create a prompt with the field content inserted into placeholders
    prompt = f"Explain the usage of the word {target_word} in the following sentence from the grammar point of view: {sentence}"

    # Send the prompt to the ChatGPT API and get the result
    try:
        result = send_prompt(prompt)
    except Exception as e:
        return showWarning(f"An error occurred while processing the note: {str(e)}")

    # Assign the result to the "ChatGPT Output" field in the note
    note["ChatGPT Output"] = result
    print("ChatGPT addon: note after chatgpt response")
    pprint(inspect.getmembers(note))
    # Save the modified note
    note.flush()


# Function to process the notes in Anki
def process_notes(browser):
    nids = browser.selectedNotes()

    if not nids:
        return tooltip("No cards selected.")

    print (browser.__class__.__name__)
    for nid in nids:
        note = mw.col.getNote(nid)
        process_note(note)


# Hook function to add the "Process Notes" menu option
def add_menu_option(browser):
    a = QAction("Process Notes with ChatGPT", browser)
    a.triggered.connect(lambda: process_notes(browser))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)


# Register the hook function to be called when setting up menus in the browser
addHook("browser.setupMenus", add_menu_option)
