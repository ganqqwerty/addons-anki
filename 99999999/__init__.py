import os
import sys
import re
from aqt import mw
from aqt.utils import showInfo, showWarning
from aqt.qt import QAction
from anki.hooks import addHook

# Add vendor directory to sys.path
addon_dir = os.path.dirname(os.path.realpath(__file__))
vendor_dir = os.path.join(addon_dir, "vendor")
sys.path.append(vendor_dir)
import openai

class ChatGPTAddon:

    def __init__(self, note, config, editor):
        self.note = note
        self.config = config
        self.editor = editor
        # Setting the API key for openai
        openai.api_key = self.config['apiKey']

    def request_data(self, prompt):
        # Call to the GPT-3 model and return the response.
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.5,
            max_tokens=60
        )
        return response

    def set_response_to_note(self, response):
        # Assuming 'text' contains the output text you want to set for the field.
        # Get the text from the response.
        text = response.choices[0].text.strip()

        target_field = self.config['targetField']
        if target_field in self.note:
            self.note[target_field] = text
        else:
            raise ValueError(f"Target field '{target_field}' not found in note.")
        self.editor.loadNoteKeepingFocus()

    def generate(self):
        try:
            note = self.note

            # Get the prompt from config and replace placeholders with actual note field values.
            prompt = self.create_prompt(self.config['prompt'], note)

            # Request data from API.
            response = self.request_data(prompt)

            # Set the response to the note.
            self.set_response_to_note(response)

        except ValueError as ve:
            # handle the error, for example, log it or display it to the user
            showWarning(f"Error: {ve}")

    def create_prompt(self, prompt, note):
        # Regex pattern for fields enclosed in triple curly brackets.
        pattern = re.compile(r"{{{(.*?)}}}")

        # Find all field placeholders in the prompt.
        fields_in_prompt = pattern.findall(prompt)

        # For each placeholder, replace it with the corresponding value from the note.
        for field in fields_in_prompt:
            if field in note:
                prompt = prompt.replace(f"{{{field}}}", note[field])
            else:
                raise ValueError(f"Field '{field}' not found in note.")

        return prompt

def process_notes(browser):
    if not browser.editor:
        raise Exception("No active editor found.")

    note = browser.editor.note
    config = mw.addonManager.getConfig(__name__)  # Get the config from the json file
    ChatGPTAddon(note, config, browser.editor).generate()

def add_menu_option(browser):
    a = QAction("Process Notes with ChatGPT", browser)
    a.triggered.connect(lambda: process_notes(browser))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

# Register the hook function to be called when setting up menus in the browser
addHook("browser.setupMenus", add_menu_option)
