import re

from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QComboBox
from aqt import mw
from aqt.utils import showWarning


class RunPromptDialog(QDialog):
    def __init__(self, parent, selected_nodes, prompt_config):
        super().__init__(parent)
        self.selected_nodes = selected_nodes
        self.result = None
        self.prompt_config = prompt_config
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.prompt_config["promptName"])
        layout = QVBoxLayout()

        self.prompt_editor = QTextEdit()
        self.prompt_editor.setPlainText(self.prompt_config["prompt"])
        self.highlight_fields(self.prompt_editor)
        self.target_field_editor = QComboBox()
        self.target_field_editor.addItems(self.get_common_fields())
        if self.prompt_config["targetField"] in self.get_common_fields():
            self.target_field_editor.setCurrentText(self.prompt_config["targetField"])

        layout.addWidget(QLabel("Prompt:"))
        layout.addWidget(self.prompt_editor)
        layout.addWidget(QLabel("Target Field:"))
        layout.addWidget(self.target_field_editor)

        run_button = QPushButton("Run")
        run_button.clicked.connect(self.try_to_accept)

        layout.addWidget(run_button)
        self.setLayout(layout)

    def get_common_fields(self):
        common_fields = set(mw.col.getNote(self.selected_nodes[0]).keys())
        for nid in self.selected_nodes:
            note = mw.col.getNote(nid)
            note_fields = set(note.keys())
            common_fields = common_fields.intersection(note_fields)
        return list(common_fields)

    def highlight_fields(self, text_editor):
        field_pattern = r'\{\{\{(.+?)\}\}\}'
        field_format = QTextCharFormat()
        field_format.setForeground(QColor('olive'))
        cursor = text_editor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        text_editor.setTextCursor(cursor)
        while cursor.position() < len(text_editor.toPlainText()):
            cursor = text_editor.document().find(field_pattern, cursor)
            if cursor.isNull():
                break
            cursor.mergeCharFormat(field_format)

    def try_to_accept(self):
        self.prompt_config["prompt"] = self.prompt_editor.toPlainText()
        self.prompt_config["targetField"] = self.target_field_editor.currentText()

        invalid_fields = get_invalid_fields_in_prompt(self.prompt_config["prompt"], self.selected_nodes)
        if invalid_fields:
            showWarning("Invalid field(s) in prompt: " + ", ".join(invalid_fields))
            return

        self.result = self.prompt_config
        self.accept()

    def get_result(self):
        return self.result


def get_invalid_fields_in_prompt(prompt, selected_notes):
    field_pattern = r'\{\{\{(.+?)\}\}\}'
    field_names = re.findall(field_pattern, prompt)
    invalid_fields = []
    for nid in selected_notes:
        note = mw.col.getNote(nid)
        for field_name in field_names:
            if field_name not in note:
                if field_name not in invalid_fields:
                    invalid_fields.append(field_name)
    return invalid_fields
