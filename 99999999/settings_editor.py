from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QComboBox, QPushButton, QTextEdit, \
    QSizePolicy, QHBoxLayout, QToolButton, QStyle
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
from aqt import mw
from PyQt5.QtWidgets import QFrame, QSizePolicy, QStyle

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
        self.emulate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Policy.Preferred)
        self.layout().addWidget(QLabel("Emulate:"))
        self.layout().addWidget(self.emulate)

    def setupPrompts(self, config):
        self.promptWidgets = []
        for i, prompt in enumerate(config["prompts"]):
            self.add_prompt_inputs(i, prompt)

        self.addPromptButton = QPushButton('Add Prompt')
        self.addPromptButton.clicked.connect(self.add_prompt)
        self.addPromptButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Policy.Preferred)
        self.layout().addWidget(self.addPromptButton)

    def add_prompt_inputs(self, i, prompt=None):
        prompt = prompt or {"prompt": "", "targetField": "", "promptName": ""}
        promptNameLabel, promptNameInput, promptLabel, promptInput, targetFieldLabel, targetFieldInput = self.create_prompt_widgets(prompt)
        removePromptButton = self.create_remove_button()
        singlePromptLayout = self.create_single_prompt_layout(promptNameLabel, promptNameInput, promptLabel, promptInput, targetFieldLabel, targetFieldInput, removePromptButton)
        self.promptWidgets.append(
            (singlePromptLayout, promptNameInput, promptInput, targetFieldInput, removePromptButton))
        removePromptButton.clicked.connect(lambda: self.remove_prompt(singlePromptLayout))


    def create_prompt_widgets(self, prompt):
        promptNameLabel = QLabel("Prompt Name:")
        promptNameInput = QLineEdit(prompt["promptName"])

        promptLabel = QLabel("Prompt:")
        promptInput = QTextEdit(prompt["prompt"])

        targetFieldLabel = QLabel("Target Field:")
        targetFieldInput = QLineEdit(prompt["targetField"])

        return promptNameLabel, promptNameInput, promptLabel, promptInput, targetFieldLabel, targetFieldInput


    def create_remove_button(self):
        removePromptButton = QToolButton()
        addon_dir = os.path.dirname(os.path.abspath(__file__))  # Get directory of current file
        icon_path = os.path.join(addon_dir, 'remove.svg')  # Create path to the icon
        removePromptButton.setIcon(QIcon(icon_path))  # Set the icon
        removePromptButton.setIconSize(QSize(24, 24))
        removePromptButton.setToolTip("Remove this prompt")
        removePromptButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Policy.Preferred)
        return removePromptButton


    def create_single_prompt_layout(self, promptNameLabel, promptNameInput, promptLabel, promptInput, targetFieldLabel, targetFieldInput, removePromptButton):
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
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            self.layout().addWidget(separator)
        self.add_prompt_inputs(len(self.promptWidgets))


    def remove_prompt(self, frame):
        for i, widgets in enumerate(self.promptWidgets):
            if widgets[0] == frame:
                # remove widgets
                for widget in widgets[1:]:
                    widget.deleteLater()
                # remove from list
                self.promptWidgets.pop(i)
                # remove frame
                frame.deleteLater()
                break


    def saveConfig(self):
        config = mw.addonManager.getConfig(__name__)
        config["apiKey"] = self.apiKey.text()
        config["emulate"] = self.emulate.currentText()

        config["prompts"] = []
        for widgets in self.promptWidgets:
            promptInput = widgets[2]
            targetFieldInput = widgets[3]
            promptNameInput = widgets[4]

            config["prompts"].append({
                "prompt": promptInput.toPlainText(),
                "targetField": targetFieldInput.text(),
                "promptName": promptNameInput.text()
            })

        mw.addonManager.writeConfig(__name__, config)
        showInfo("Configuration saved.")
        self.close()
