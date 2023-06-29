def format_response_and_fill_field(response, note, target_field):
    """Format response and fill the target field in the note."""
    if response is None:
        return

    formatted_response = response.replace("\n", "<br>")

    if target_field in note:
        note[target_field] = formatted_response
    else:
        raise ValueError(f"Target field '{target_field}' not found in note.")


def fill_field_for_note_in_editor(response, target_field, editor):
    """Set response to the editor's note."""
    format_response_and_fill_field(response, editor.note, target_field)
    editor.loadNoteKeepingFocus()


def fill_field_for_note_not_in_editor(response, note, target_field):
    """Set response to the note."""
    format_response_and_fill_field(response, note, target_field)
    note.flush()
