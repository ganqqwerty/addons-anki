from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtWidgets import QWidget, QDialog
from PyQt6.QtCore import QSize
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo

from .prompt_ui import Ui_Form
from .settings_window_ui import Ui_SettingsWindow
import json

class PromptWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        addon_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(addon_dir, 'remove.svg')
        self.removePromptButton.setIcon(QIcon(icon_path))
        self.removePromptButton.setIconSize(QSize(24, 24))


class SettingsWindow(QDialog, Ui_SettingsWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.setWindowTitle('ChatGPT Settings')
        config = mw.addonManager.getConfig(__name__)
        self.setup_config(config)
        self.saveButton.clicked.connect(self.saveConfig)

    def setWindowSize(self):
        screen_size = QGuiApplication.primaryScreen().geometry()
        self.resize(screen_size.width() * 0.8, screen_size.height() * 0.8)

    def setup_config(self, config):
        self.apiKey.setText(config.get("apiKey", ""))
        self.anthropicKey.setText(config.get("anthropicKey", ""))
        self.selectedApi.setCurrentText(config.get("selectedApi", "openai"))
        self.emulate.setCurrentText(config.get("emulate", "no"))
        
        self.promptWidgets = []
        for prompt in config.get("prompts", []):
            self.add_prompt(prompt)

    def add_prompt(self, prompt):
        promptWidget = PromptWidget()
        promptWidget.promptInput.setPlainText(prompt["prompt"])
        promptWidget.targetFieldInput.setText(prompt["targetField"])
        promptWidget.promptNameInput.setText(prompt["promptName"])
        promptWidget.removePromptButton.clicked.connect(
            lambda: self.remove_prompt(promptWidget))
        
        self.promptsLayout.addWidget(promptWidget)
        self.promptWidgets.append(promptWidget)

    def remove_prompt(self, promptWidgetToRemove):
        self.promptWidgets.remove(promptWidgetToRemove)
        self.promptsLayout.removeWidget(promptWidgetToRemove)
        promptWidgetToRemove.deleteLater()

    def saveConfig(self):
        config = mw.addonManager.getConfig(__name__)
        
        config["apiKey"] = self.apiKey.text()
        config["anthropicKey"] = self.anthropicKey.text()
        config["selectedApi"] = self.selectedApi.currentText()
        config["emulate"] = self.emulate.currentText()
        
        config["prompts"] = []
        for promptWidget in self.promptWidgets:
            promptInput = promptWidget.promptInput
            targetFieldInput = promptWidget.targetFieldInput
            promptNameInput = promptWidget.promptNameInput
            
            config["prompts"].append({
                "prompt": promptInput.toPlainText(),
                "targetField": targetFieldInput.text(),
                "promptName": promptNameInput.text()
            })
        
        mw.addonManager.writeConfig(__name__, config)
        showInfo("Configuration saved.")
        self.close()
