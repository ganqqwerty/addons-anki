from aqt import mw
from aqt.qt import *
from aqt.gui_hooks import editor_did_init_buttons
from aqt.editor import EditorMode, Editor
from aqt.browser import Browser
from aqt.editcurrent import EditCurrent
from aqt.addcards import AddCards
from anki.hooks import addHook
import os

from .settings_editor import SettingsWindow
from .process_notes import process_notes, generate_for_single_note
from .run_prompt_dialog import RunPromptDialog
from aqt.utils import showWarning

ADDON_NAME = 'IntelliFiller'

def get_common_fields(selected_nodes_ids):
    common_fields = set(mw.col.getNote(selected_nodes_ids[0]).keys())
    for nid in selected_nodes_ids:
        note = mw.col.getNote(nid)
        note_fields = set(note.keys())
        common_fields = common_fields.intersection(note_fields)
    return list(common_fields)

def create_run_prompt_dialog_from_browser(browser, prompt_config):
    common_fields = get_common_fields(browser.selectedNotes())
    dialog = RunPromptDialog(browser, common_fields, prompt_config)
    if dialog.exec_() == QDialog.DialogCode.Accepted:
        updated_prompt_config = dialog.get_result()
        process_notes(browser, updated_prompt_config)

def handle_browser_mode(editor: Editor, prompt_config):
    browser: Browser = editor.parentWindow
    common_fields = get_common_fields(browser.selectedNotes())
    dialog = RunPromptDialog(browser, common_fields, prompt_config)
    if dialog.exec_() == QDialog.DialogCode.Accepted:
        updated_prompt_config = dialog.get_result()
        process_notes(browser, updated_prompt_config)

def handle_edit_current_mode(editor: Editor, prompt_config):
    editCurrentWindow: EditCurrent = editor.parentWindow
    common_fields = get_common_fields([editor.note.id])
    dialog = RunPromptDialog(editCurrentWindow, common_fields, prompt_config)
    if dialog.exec_() == QDialog.DialogCode.Accepted:
        updated_prompt_config = dialog.get_result()
        generate_for_single_note(editor, updated_prompt_config)

def handle_add_cards_mode(editor: Editor, prompt_config):
    addCardsWindow: AddCards = editor.parentWindow
    keys = editor.note.keys()
    dialog = RunPromptDialog(addCardsWindow, keys, prompt_config)
    if dialog.exec_() == QDialog.DialogCode.Accepted:
        updated_prompt_config = dialog.get_result()
        generate_for_single_note(editor, updated_prompt_config)

def create_run_prompt_dialog_from_editor(editor: Editor, prompt_config):
    if editor.editorMode == EditorMode.BROWSER:
        handle_browser_mode(editor, prompt_config)
    elif editor.editorMode == EditorMode.EDIT_CURRENT:
        handle_edit_current_mode(editor, prompt_config)
    elif editor.editorMode == EditorMode.ADD_CARDS:
        handle_add_cards_mode(editor, prompt_config)

def add_context_menu_items(browser, menu):
    submenu = QMenu(ADDON_NAME, menu)
    menu.addMenu(submenu)
    config = mw.addonManager.getConfig(__name__)

    for prompt_config in config['prompts']:
        action = QAction(prompt_config["promptName"], browser)
        action.triggered.connect(lambda _, br=browser, pc=prompt_config: create_run_prompt_dialog_from_browser(br, pc))
        submenu.addAction(action)


def open_settings():
    window = SettingsWindow(mw)
    window.exec_()


def on_editor_button(editor):
    prompts = mw.addonManager.getConfig(__name__).get('prompts', [])

    menu = QMenu(editor.widget)
    for i, prompt in enumerate(prompts):
        action = QAction(f'Prompt {i + 1}: {prompt["promptName"]}', menu)
        action.triggered.connect(lambda _, p=prompt: create_run_prompt_dialog_from_editor(editor, p))
        menu.addAction(action)

    menu.exec_(editor.widget.mapToGlobal(QPoint(0, 0)))


def on_setup_editor_buttons(buttons, editor):
    icon_path = os.path.join(os.path.dirname(__file__), "icon.svg")
    btn = editor.addButton(
        icon=icon_path,
        cmd="run_prompt",
        func=lambda e=editor: on_editor_button(e),
        tip=ADDON_NAME,
        keys=None,
        disables=False
    )
    buttons.append(btn)
    return buttons


addHook("browser.onContextMenu", add_context_menu_items)
mw.addonManager.setConfigAction(__name__, open_settings)
editor_did_init_buttons.append(on_setup_editor_buttons)
