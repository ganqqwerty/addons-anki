import os
import re
import sys

from aqt import mw
from aqt.utils import showWarning

config = mw.addonManager.getConfig(__name__)

addon_dir = os.path.dirname(os.path.realpath(__file__))
vendor_dir = os.path.join(addon_dir, "vendor")
sys.path.append(vendor_dir)
import openai

openai.api_key = config['apiKey']

def generate_for_single_note(editor, prompt_config):
    """Generate text for a single note (editor note)."""
    prompt = create_prompt(editor.note, prompt_config)
    response = send_prompt_to_openai(prompt)

    target_field = prompt_config['targetField']
    fill_field_for_note_in_editor(response, target_field, editor)


def generate_for_multiple_notes(nid, prompt_config):
    """Generate text for multiple notes."""
    note = mw.col.getNote(nid)
    prompt = create_prompt(note, prompt_config)
    response = send_prompt_to_openai(prompt)
    set_response_to_note(response, note, prompt_config)


def create_prompt(note, prompt_config):
    prompt_template = prompt_config['prompt']
    pattern = re.compile(r'\{\{\{(\w+)\}\}\}')
    field_names = pattern.findall(prompt_template)
    for field_name in field_names:
        if field_name not in note:
            raise ValueError(f"Field '{field_name}' not found in note.")
        prompt_template = prompt_template.replace(f'{{{field_name}}}', note[field_name])
    return prompt_template


def send_prompt_to_openai(prompt):
    if config.get('emulate') == 'yes':
        return "This is a fake response for emulation mode."

    try:
        response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100)
        return response.choices[0].text.strip()
    except Exception as e:
        showWarning(f"An error occurred while processing the note: {str(e)}")
        return None


def fill_field_for_note_in_editor(response, target_field, editor ):
    """Set response to the editor's note."""
    if response is None:
        return

    if target_field in editor.note:
        editor.note[target_field] = response
    else:
        raise ValueError(f"Target field '{target_field}' not found in note.")

    editor.loadNoteKeepingFocus()


def set_response_to_note(response, note, prompt_config):
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

    if len(selected_notes) == 1 and browser.editor and browser.editor.note:
        generate_for_single_note(browser.editor, prompt_config)
    else:
        for nid in selected_notes:
            generate_for_multiple_notes(nid, prompt_config)
