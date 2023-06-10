from PyQt5.QtWidgets import QFrame, QSizePolicy
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QLabel, QComboBox, QPushButton, QHBoxLayout, QToolButton
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
from .prompt_ui import Ui_Form  # import the class from your generated Python file


class PromptWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # this sets up the layout and widgets according to your design


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('ChatGPT Settings')
        self.setLayout(QVBoxLayout())

        self.setWindowSize()

        config = mw.addonManager.getConfig(__name__)

        self.setupApiKey(config)
        self.setupEmulate(config)
        self.setupPrompts(config)

        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(self.saveConfig)
        self.saveButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.layout().addWidget(self.saveButton)

    def setWindowSize(self):
        # Get screen size
        screen_size = QGuiApplication.primaryScreen().geometry()

        # Set window size to be 80% of screen width and height
        self.resize(screen_size.width() * 0.8, screen_size.height() * 0.8)

    def setupApiKey(self, config):
        self.apiKey = QLineEdit(config["apiKey"])
        self.apiKey.setPlaceholderText("API key")
        self.layout().addWidget(QLabel("API Key:"))
        self.layout().addWidget(self.apiKey)

    def setupEmulate(self, config):
        self.emulate = QComboBox()
        self.emulate.addItem("yes")
        self.emulate.addItem("no")
        self.emulate.setCurrentText(config["emulate"])
        self.emulate.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        self.layout().addWidget(QLabel("Emulate:"))
        self.layout().addWidget(self.emulate)

    def setupPrompts(self, config):
        self.promptWidgets = []
        for i, prompt in enumerate(config["prompts"]):
            self.add_prompt_inputs(i, prompt)
        self.addPromptButton = QPushButton('Add Prompt')
        self.addPromptButton.clicked.connect(self.add_prompt)
        self.layout().addWidget(self.addPromptButton)

    def add_prompt_inputs(self, i, prompt=None):
        if prompt is None:
            prompt = {"prompt": "", "targetField": "", "promptName": ""}

        promptWidget = PromptWidget()
        promptWidget.promptInput.setPlainText(prompt["prompt"])
        promptWidget.targetFieldInput.setText(prompt["targetField"])
        promptWidget.promptNameInput.setText(prompt["promptName"])
        promptWidget.removePromptButton.clicked.connect(lambda: self.remove_prompt(promptWidget))

        self.layout().insertWidget(i, promptWidget)
        self.promptWidgets.append(promptWidget)


    def create_remove_button(self):
        removePromptButton = QToolButton()
        addon_dir = os.path.dirname(os.path.abspath(__file__))  # Get directory of current file
        icon_path = os.path.join(addon_dir, 'remove.svg')  # Create path to the icon
        removePromptButton.setIcon(QIcon(icon_path))  # Set the icon
        removePromptButton.setIconSize(QSize(24, 24))
        removePromptButton.setToolTip("Remove this prompt")
        removePromptButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Policy.Preferred)
        return removePromptButton

    def create_single_prompt_layout(self, promptNameLabel, promptNameInput, promptLabel, promptInput, targetFieldLabel,
                                    targetFieldInput, removePromptButton):
        promptLayout = QVBoxLayout()
        promptLayout.addWidget(promptNameLabel)
        promptLayout.addWidget(promptNameInput)
        promptLayout.addWidget(promptLabel)
        promptLayout.addWidget(promptInput)
        promptLayout.addWidget(targetFieldLabel)
        promptLayout.addWidget(targetFieldInput)

        singlePromptLayout = QHBoxLayout()
        singlePromptLayout.addLayout(promptLayout)
        singlePromptLayout.addWidget(removePromptButton)

        # Add a frame around the prompt layout
        frame = QFrame()
        frame.setLayout(singlePromptLayout)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)

        self.layout().addWidget(frame)
        return frame

    def add_prompt(self):
        # Before adding a new prompt, add a separator
        if self.promptWidgets:
            separator = QFrame()
            separator.setFrameShape(QFrame.Shape.HLine)
            separator.setFrameShadow(QFrame.Shadow.Sunken)
            self.layout().addWidget(separator)
        self.add_prompt_inputs(len(self.promptWidgets))

    def remove_prompt(self, promptWidgetToRemove):
        for i, promptWidget in enumerate(self.promptWidgets):
            if promptWidget == promptWidgetToRemove:
                # remove widget
                promptWidget.deleteLater()
                # remove from list
                self.promptWidgets.pop(i)
                break


    def saveConfig(self):
        config = mw.addonManager.getConfig(__name__)
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

        mw.addonManager.writeConfig(__name__, config)
        showInfo("Configuration saved.")
        self.close()
