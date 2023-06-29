import re

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QComboBox
from aqt import mw
from aqt.utils import showWarning


class RunPromptDialog(QDialog):
    def __init__(self, parentWindow, selected_nodes_ids, prompt_config):
        super().__init__(parentWindow)
        self.selected_nodes_ids = selected_nodes_ids
        self.result = None
        self.prompt_config = prompt_config
        self.setupLayout()

    def setupLayout(self):
        self.setWindowTitle(self.prompt_config["promptName"])
        layout = QVBoxLayout()

        self.prompt_editor = QTextEdit()
        self.prompt_editor.setPlainText(self.prompt_config["prompt"])

        self.target_field_editor = QComboBox()
        self.common_fields = get_common_fields(self.selected_nodes_ids)
        self.target_field_editor.addItems(self.common_fields)
        if self.prompt_config["targetField"] in self.common_fields:
            self.target_field_editor.setCurrentText(self.prompt_config["targetField"])

        layout.addWidget(QLabel("Prompt:"))
        layout.addWidget(self.prompt_editor)
        layout.addWidget(QLabel("Target Field:"))
        layout.addWidget(self.target_field_editor)

        run_button = QPushButton("Run")
        run_button.clicked.connect(self.try_to_accept)

        layout.addWidget(run_button)
        self.setLayout(layout)

    def try_to_accept(self):
        self.prompt_config["prompt"] = self.prompt_editor.toPlainText()
        self.prompt_config["targetField"] = self.target_field_editor.currentText()

        invalid_fields = get_invalid_fields_in_prompt(self.prompt_config["prompt"], self.common_fields)
        if invalid_fields:
            showWarning("Invalid field(s) in prompt: " + ", ".join(invalid_fields))
            return

        self.result = self.prompt_config
        self.accept()

    def get_result(self):
        return self.result


def get_invalid_fields_in_prompt(prompt, common_field_names):
    field_pattern = r'\{\{\{(.+?)\}\}\}'
    prompt_field_names = re.findall(field_pattern, prompt)
    pf_names_set = set(prompt_field_names)
    cf_names_set = set(common_field_names)
    return pf_names_set.difference(cf_names_set)


def get_common_fields(selected_nodes_ids):
    common_fields = set(mw.col.getNote(selected_nodes_ids[0]).keys())
    for nid in selected_nodes_ids:
        note = mw.col.getNote(nid)
        note_fields = set(note.keys())
        common_fields = common_fields.intersection(note_fields)
    return list(common_fields)