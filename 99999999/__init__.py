import os
import sys
import json
import re
from typing import Dict
from PyQt5.QtWidgets import QAction
from aqt import mw
from aqt.utils import showWarning
from anki.hooks import addHook

addon_dir = os.path.dirname(os.path.realpath(__file__))
vendor_dir = os.path.join(addon_dir, "vendor")
sys.path.append(vendor_dir)
import openai


class ChatGPTAddon:
    def __init__(self, config):
        self.config = config
        openai.api_key = self.config['apiKey']

    def generate_for_single_note(self, browser, prompt_config):
        """Generate text for a single note (editor note)."""
        prompt = self.create_prompt(browser.editor.note, prompt_config)
        response = self.send_prompt_to_openai(prompt)
        self.set_response_to_editor_note(response, browser, prompt_config)

    def generate_for_multiple_notes(self, nid, prompt_config):
        """Generate text for multiple notes."""
        note = mw.col.getNote(nid)
        prompt = self.create_prompt(note, prompt_config)
        response = self.send_prompt_to_openai(prompt)
        self.set_response_to_note(response, note, prompt_config)

    def create_prompt(self, note, prompt_config):
        prompt_template = prompt_config['prompt']
        pattern = re.compile(r'\{\{\{(\w+)\}\}\}')
        field_names = pattern.findall(prompt_template)
        for field_name in field_names:
            if field_name not in note:
                raise ValueError(f"Field '{field_name}' not found in note.")
            prompt_template = prompt_template.replace(f'{{{field_name}}}', note[field_name])
        return prompt_template

    def send_prompt_to_openai(self, prompt):
        if self.config.get('emulate') == 'yes':
            return "This is a fake response for emulation mode."

        try:
            response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100)
            return response.choices[0].text.strip()
        except Exception as e:
            showWarning(f"An error occurred while processing the note: {str(e)}")
            return None

    def set_response_to_editor_note(self, response, browser, prompt_config):
        """Set response to the editor's note."""
        if response is None:
            return

        target_field = prompt_config['targetField']
        if target_field in browser.editor.note:
            browser.editor.note[target_field] = response
        else:
            raise ValueError(f"Target field '{target_field}' not found in note.")

        browser.editor.loadNoteKeepingFocus()

    def set_response_to_note(self, response, note, prompt_config):
        """Set response to the note."""
        if response is None:
            return

        target_field = prompt_config['targetField']
        if target_field in note:
            note[target_field] = response
        else:
            raise ValueError(f"Target field '{target_field}' not found in note.")

        note.flush()

def process_notes(browser, prompt_config):
    selected_notes = browser.selectedNotes()
    if not selected_notes:
        showWarning("No notes selected.")
        return

    config = mw.addonManager.getConfig(__name__)
    chatGPTAddon = ChatGPTAddon(config)
    if len(selected_notes) == 1 and browser.editor and browser.editor.note:
        chatGPTAddon.generate_for_single_note(browser, prompt_config)
    else:
        for nid in selected_notes:
            chatGPTAddon.generate_for_multiple_notes(nid, prompt_config)

def add_menu_option(browser):
    config = mw.addonManager.getConfig(__name__)
    for prompt_config in config['prompts']:
        a = QAction(prompt_config["promptName"], browser)
        a.triggered.connect(lambda _, prompt_config=prompt_config: process_notes(browser, prompt_config))
        browser.form.menuEdit.addSeparator()
        browser.form.menuEdit.addAction(a)

addHook("browser.setupMenus", add_menu_option)
