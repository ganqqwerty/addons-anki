
from aqt import mw
from aqt.utils import showWarning

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
    set_response_to_note(response, note, prompt_config)


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
