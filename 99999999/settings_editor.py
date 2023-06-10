from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QComboBox, QTableWidget, QHeaderView, QPushButton, \
    QTextEdit
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('ChatGPT Settings')
        self.setLayout(QVBoxLayout())

        # Get screen size
        screen_size = QGuiApplication.primaryScreen().geometry()

        # Set window size to be 80% of screen width
        self.resize(screen_size.width() * 0.8, screen_size.height() * 0.8)

        config = mw.addonManager.getConfig(__name__)

        self.apiKey = QLineEdit(config["apiKey"])
        self.apiKey.setPlaceholderText("API key")
        self.layout().addWidget(QLabel("API Key:"))
        self.layout().addWidget(self.apiKey)

        self.emulate = QComboBox()
        self.emulate.addItem("yes")
        self.emulate.addItem("no")
        self.emulate.setCurrentText(config["emulate"])
        self.layout().addWidget(QLabel("Emulate:"))
        self.layout().addWidget(self.emulate)

        self.promptsTable = QTableWidget()
        self.promptsTable.setColumnCount(3)
        self.promptsTable.setHorizontalHeaderLabels(["Prompt", "Target Field", "Prompt Name"])
        self.promptsTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.promptsTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for i, prompt in enumerate(config["prompts"]):
            self.add_prompt_inputs(i, prompt)

        self.layout().addWidget(QLabel("Prompts:"))
        self.layout().addWidget(self.promptsTable)

        self.addPromptButton = QPushButton('Add Prompt')
        self.addPromptButton.clicked.connect(self.add_prompt)
        self.layout().addWidget(self.addPromptButton)

        self.removePromptButton = QPushButton('Remove Prompt')
        self.removePromptButton.clicked.connect(self.remove_prompt)
        self.layout().addWidget(self.removePromptButton)

        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(self.saveConfig)
        self.layout().addWidget(self.saveButton)

    def add_prompt_inputs(self, i, prompt=None):
        prompt = prompt or {"prompt": "", "targetField": "", "promptName": ""}

        promptInput = QTextEdit(prompt["prompt"])
        targetFieldInput = QLineEdit(prompt["targetField"])
        promptNameInput = QLineEdit(prompt["promptName"])

        self.promptsTable.setRowCount(self.promptsTable.rowCount() + 1)
        self.promptsTable.setCellWidget(i, 0, promptInput)
        self.promptsTable.setCellWidget(i, 1, targetFieldInput)
        self.promptsTable.setCellWidget(i, 2, promptNameInput)

    def add_prompt(self):
        i = self.promptsTable.rowCount()
        self.add_prompt_inputs(i)

    def remove_prompt(self):
        if self.promptsTable.rowCount() > 0:
            self.promptsTable.removeRow(self.promptsTable.rowCount() - 1)

    def saveConfig(self):
        config = mw.addonManager.getConfig(__name__)
        config["apiKey"] = self.apiKey.text()
        config["emulate"] = self.emulate.currentText()

        config["prompts"] = []
        for i in range(self.promptsTable.rowCount()):
            promptInput = self.promptsTable.cellWidget(i, 0)
            targetFieldInput = self.promptsTable.cellWidget(i, 1)
            promptNameInput = self.promptsTable.cellWidget(i, 2)

            config["prompts"].append({
                "prompt": promptInput.toPlainText(),
                "targetField": targetFieldInput.text(),
                "promptName": promptNameInput.text()
            })

        mw.addonManager.writeConfig(__name__, config)
        showInfo("Configuration saved.")
        self.close()
