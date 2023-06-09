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



from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle("Anki AI Add-on Settings")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.config = mw.addonManager.getConfig(__name__)

        self.api_key_input = QLineEdit(self.config['apiKey'])
        self.layout.addWidget(QLabel("API Key:"))
        self.layout.addWidget(self.api_key_input)

        self.emulate_combobox = QComboBox()
        self.emulate_combobox.addItems(["yes", "no"])
        self.emulate_combobox.setCurrentText(self.config['emulate'])
        self.layout.addWidget(QLabel("Emulate mode:"))
        self.layout.addWidget(self.emulate_combobox)

        self.layout.addWidget(QLabel("Prompts:"))

        self.prompts_layout = QVBoxLayout()
        self.layout.addLayout(self.prompts_layout)

        self.prompts_inputs = []
        for prompt in self.config['prompts']:
            self.add_prompt_inputs(prompt)

        add_prompt_button = QPushButton("Add Prompt")
        add_prompt_button.clicked.connect(self.add_prompt_inputs)
        self.layout.addWidget(add_prompt_button)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def add_prompt_inputs(self, prompt=None):
        layout = QHBoxLayout()
        self.prompts_layout.addLayout(layout)

        prompt_name_input = QLineEdit(prompt['promptName'] if prompt else "")
        prompt_input = QLineEdit(prompt['prompt'] if prompt else "")
        target_field_input = QLineEdit(prompt['targetField'] if prompt else "")

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(prompt_name_input)
        layout.addWidget(QLabel("Prompt:"))
        layout.addWidget(prompt_input)
        layout.addWidget(QLabel("Target Field:"))
        layout.addWidget(target_field_input)

        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.remove_prompt_inputs(layout))
        layout.addWidget(remove_button)

        self.prompts_inputs.append((prompt_name_input, prompt_input, target_field_input))

    def remove_prompt_inputs(self, layout):
        for i in reversed(range(layout.count())):  # remove widgets
            widget = layout.itemAt(i).widget()
            layout.removeWidget(widget)
            widget.setParent(None)
        self.prompts_layout.removeItem(layout)  # remove layout

        # remove from prompts_inputs
        for inputs in self.prompts_inputs:
            if inputs[0].parent() is None:  # if the QLineEdit for the prompt name has been removed
                self.prompts_inputs.remove(inputs)
                break

    def accept(self):
        self.config['apiKey'] = self.api_key_input.text()
        self.config['emulate'] = self.emulate_combobox.currentText()
        self.config['prompts'] = [{'promptName': inputs[0].text(), 'prompt': inputs[1].text(), 'targetField': inputs[2].text()}
                                  for inputs in self.prompts_inputs]
        mw.addonManager.writeConfig(__name__, self.config)
        super(SettingsDialog, self).accept()


def open_settings():
    dialog = SettingsDialog()
    dialog.exec_()


mw.addonManager.setConfigAction(__name__, open_settings)
