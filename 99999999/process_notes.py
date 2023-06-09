
from aqt import mw
from aqt.utils import showWarning

from .modify_notes import fill_field_for_note_in_editor, fill_field_for_note_not_in_editor
from .data_request import create_prompt, send_prompt_to_openai

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
    fill_field_for_note_not_in_editor(response, note, prompt_config)


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
