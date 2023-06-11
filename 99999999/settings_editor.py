from PyQt5.QtGui import QGuiApplication
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo

from .prompt_ui import Ui_Form  # Import the class from your generated Python file
from .settings_window_ui import Ui_SettingsWindow
import json

class PromptWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # this sets up the layout and widgets according to your design

        # Set SVG icon for the remove button
        addon_dir = os.path.dirname(os.path.abspath(__file__))  # Get directory of current file
        icon_path = os.path.join(addon_dir, 'remove.svg')  # Create path to the icon
        self.removePromptButton.setIcon(QIcon(icon_path))  # Set the icon
        self.removePromptButton.setIconSize(QSize(24, 24))  # Set icon size # this sets up the layout and widgets according to your design


class SettingsWindow(QDialog, Ui_SettingsWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Set up the layout and widgets from the UI file

        self.setWindowTitle('ChatGPT Settings')
        # self.setWindowSize()

        config = mw.addonManager.getConfig(__name__)

        self.setup_config(config)

        self.saveButton.clicked.connect(self.saveConfig)

    def setWindowSize(self):
        # Get screen size
        screen_size = QGuiApplication.primaryScreen().geometry()

        # Set window size to be 80% of screen width and height
        self.resize(screen_size.width() * 0.8, screen_size.height() * 0.8)

    def setup_config(self, config):
        self.apiKey.setText(config["apiKey"])
        self.emulate.setCurrentText(config["emulate"])

        self.promptWidgets = []
        for i, prompt in enumerate(config["prompts"]):
            self.add_prompt(prompt)

        self.addPromptButton.clicked.connect(lambda: self.add_prompt({"prompt": "", "targetField": "", "promptName": ""}))

    def add_prompt(self, prompt):
        promptWidget = PromptWidget()
        promptWidget.promptInput.setPlainText(prompt["prompt"])
        promptWidget.targetFieldInput.setText(prompt["targetField"])
        promptWidget.promptNameInput.setText(prompt["promptName"])
        promptWidget.removePromptButton.clicked.connect(lambda: self.remove_prompt(promptWidget))

        self.promptsLayout.addWidget(promptWidget)
        self.promptWidgets.append(promptWidget)

    def remove_prompt(self, promptWidgetToRemove):
        self.promptWidgets.remove(promptWidgetToRemove)
        self.promptsLayout.removeWidget(promptWidgetToRemove)
        promptWidgetToRemove.deleteLater()

    def saveConfig(self):
        config = mw.addonManager.getConfig(__name__)
        print("existing config")
        print(json.dumps(config, indent=4))

        config["apiKey"] = self.apiKey.text()
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

        print ("config right before write")
        print(json.dumps(config, indent=4))
        mw.addonManager.writeConfig(__name__, config)
        showInfo("Configuration saved.")
        self.close()
