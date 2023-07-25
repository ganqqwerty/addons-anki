import logging


def format_response_and_fill_field(response, note, target_field):
    """Format response and fill the target field in the note."""
    if response is None:
        logging.error("response in null for some reason")
        return

    formatted_response = response.replace("\n", "<br>")

    if target_field in note:
        note[target_field] = formatted_response
        logging.debug("filled the field %s", target_field)
    else:
        logging.error(f"Target field '{target_field}' not found in note.")
        raise ValueError(f"Target field '{target_field}' not found in note.")


def fill_field_for_note_in_editor(response, target_field, editor):
    """Set response to the editor's note."""
    logging.debug("trying to fill field in editor")
    format_response_and_fill_field(response, editor.note, target_field)
    editor.loadNoteKeepingFocus()
    logging.debug("the editor should be updated")


def fill_field_for_note_not_in_editor(response, note, target_field):
    """Set response to the note."""
    logging.debug("trying to fill field without editor")
    format_response_and_fill_field(response, note, target_field)
    note.flush()
    logging.debug("note is flushed and the changes are supposed to be recorded in the database")
    ## how about adding the check that the changes are commited by selecting the note from the db?
