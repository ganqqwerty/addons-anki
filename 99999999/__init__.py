from PyQt5.QtWidgets import QAction, QMenu, QDialog
from anki.hooks import addHook

from .process_notes import process_notes
from aqt import mw

ADDON_NAME = 'Anki AI Add-on'

from .run_prompt_dialog import RunPromptDialog


def create_run_prompt_dialog(browser, prompt_config):
    dialog = RunPromptDialog(browser, browser.selectedNotes(), prompt_config)
    if dialog.exec_() == QDialog.DialogCode.Accepted:
        updated_prompt_config = dialog.get_result()
        process_notes(browser, updated_prompt_config)


def add_prompts_as_context_menu_items(browser, menu):
    submenu = QMenu(ADDON_NAME, menu)
    menu.addMenu(submenu)
    config = mw.addonManager.getConfig(__name__)

    for prompt_config in config['prompts']:
        a = QAction(prompt_config["promptName"], browser)
        a.triggered.connect(
            lambda _, br=browser, pc=prompt_config:
            create_run_prompt_dialog(br, pc)
        )
        submenu.addAction(a)


addHook("browser.onContextMenu", add_prompts_as_context_menu_items)
