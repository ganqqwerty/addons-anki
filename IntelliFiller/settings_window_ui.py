# -*- coding: utf-8 -*-

from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.setWindowModality(QtCore.Qt.WindowModality.NonModal)
        SettingsWindow.resize(805, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, 
                                         QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingsWindow.sizePolicy().hasHeightForWidth())
        SettingsWindow.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(SettingsWindow)
        self.verticalLayout.setObjectName("verticalLayout")

        # OpenAI API Key
        self.labelApiKey = QtWidgets.QLabel(SettingsWindow)
        self.labelApiKey.setObjectName("labelApiKey")
        self.verticalLayout.addWidget(self.labelApiKey)
        self.apiKey = QtWidgets.QLineEdit(SettingsWindow)
        self.apiKey.setObjectName("apiKey")
        self.verticalLayout.addWidget(self.apiKey)

        # Anthropic API Key
        self.labelAnthropicKey = QtWidgets.QLabel(SettingsWindow)
        self.labelAnthropicKey.setObjectName("labelAnthropicKey")
        self.verticalLayout.addWidget(self.labelAnthropicKey)
        self.anthropicKey = QtWidgets.QLineEdit(SettingsWindow)
        self.anthropicKey.setObjectName("anthropicKey")
        self.verticalLayout.addWidget(self.anthropicKey)

        # API Selection
        self.labelSelectedApi = QtWidgets.QLabel(SettingsWindow)
        self.labelSelectedApi.setObjectName("labelSelectedApi")
        self.verticalLayout.addWidget(self.labelSelectedApi)
        self.selectedApi = QtWidgets.QComboBox(SettingsWindow)
        self.selectedApi.setObjectName("selectedApi")
        self.selectedApi.addItem("openai")
        self.selectedApi.addItem("anthropic")
        self.verticalLayout.addWidget(self.selectedApi)

        # Emulate
        self.labelEmulate = QtWidgets.QLabel(SettingsWindow)
        self.labelEmulate.setObjectName("labelEmulate")
        self.verticalLayout.addWidget(self.labelEmulate)
        self.emulate = QtWidgets.QComboBox(SettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, 
                                         QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.emulate.sizePolicy().hasHeightForWidth())
        self.emulate.setSizePolicy(sizePolicy)
        self.emulate.setObjectName("emulate")
        self.emulate.addItem("")
        self.emulate.addItem("")
        self.verticalLayout.addWidget(self.emulate)

        # Prompts
        self.addPromptButton = QtWidgets.QPushButton(SettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, 
                                         QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addPromptButton.sizePolicy().hasHeightForWidth())
        self.addPromptButton.setSizePolicy(sizePolicy)
        self.addPromptButton.setObjectName("addPromptButton")
        self.verticalLayout.addWidget(self.addPromptButton)

        self.scrollArea = QtWidgets.QScrollArea(SettingsWindow)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 779, 605))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.promptsLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.promptsLayout.setObjectName("promptsLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.saveButton = QtWidgets.QPushButton(SettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, 
                                         QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout.addWidget(self.saveButton, 0, QtCore.Qt.AlignmentFlag.AlignRight)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "IntelliFiller Settings"))
        self.labelApiKey.setText(_translate("SettingsWindow", "OpenAI API Key:"))
        self.apiKey.setPlaceholderText(_translate("SettingsWindow", "OpenAI API key"))
        self.labelAnthropicKey.setText(_translate("SettingsWindow", "Anthropic API Key:"))
        self.anthropicKey.setPlaceholderText(_translate("SettingsWindow", "Anthropic API key"))
        self.labelSelectedApi.setText(_translate("SettingsWindow", "Selected API:"))
        self.labelEmulate.setText(_translate("SettingsWindow", "Emulate:"))
        self.emulate.setItemText(0, _translate("SettingsWindow", "yes"))
        self.emulate.setItemText(1, _translate("SettingsWindow", "no"))
        self.addPromptButton.setText(_translate("SettingsWindow", "Add Prompt"))
        self.saveButton.setText(_translate("SettingsWindow", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingsWindow = QtWidgets.QDialog()
    ui = Ui_SettingsWindow()
    ui.setupUi(SettingsWindow)
    SettingsWindow.show()
    sys.exit(app.exec())