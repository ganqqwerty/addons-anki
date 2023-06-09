def fill_field_for_note_in_editor(response, target_field, editor):
    """Set response to the editor's note."""
    if response is None:
        return

    if target_field in editor.note:
        editor.note[target_field] = response
    else:
        raise ValueError(f"Target field '{target_field}' not found in note.")

    editor.loadNoteKeepingFocus()


def fill_field_for_note_not_in_editor(response, note, prompt_config):
    """Set response to the note."""
    if response is None:
        return

    target_field = prompt_config['targetField']
    if target_field in note:
        note[target_field] = response
    else:
        raise ValueError(f"Target field '{target_field}' not found in note.")

    note.flush()
