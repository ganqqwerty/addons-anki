from PyQt5.QtWidgets import QAction, QMenu, QDialog
from aqt import mw
from aqt.qt import *
from aqt.gui_hooks import editor_did_init_buttons
from anki.hooks import addHook
import os

from .settings_editor import SettingsWindow
from .process_notes import process_notes
from .run_prompt_dialog import RunPromptDialog


ADDON_NAME = 'IntelliFiller'


def create_run_prompt_dialog(browser, prompt_config):
    dialog = RunPromptDialog(browser, browser.selectedNotes(), prompt_config)
    if dialog.exec_() == QDialog.DialogCode.Accepted:
        updated_prompt_config = dialog.get_result()
        process_notes(browser, updated_prompt_config)


def add_context_menu_items(browser, menu):
    submenu = QMenu(ADDON_NAME, menu)
    menu.addMenu(submenu)
    config = mw.addonManager.getConfig(__name__)

    for prompt_config in config['prompts']:
        action = QAction(prompt_config["promptName"], browser)
        action.triggered.connect(lambda _, br=browser, pc=prompt_config: create_run_prompt_dialog(br, pc))
        submenu.addAction(action)


def open_settings():
    window = SettingsWindow(mw)
    window.exec_()


def on_editor_button(editor):
    prompts = mw.addonManager.getConfig(__name__).get('prompts', [])

    menu = QMenu(editor.widget)
    for i, prompt in enumerate(prompts):
        action = QAction(f'Prompt {i + 1}: {prompt["promptName"]}', menu)
        action.triggered.connect(lambda _, p=prompt: create_run_prompt_dialog(editor.parentWindow, p))
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
