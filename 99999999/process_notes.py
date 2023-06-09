from aqt import mw
from aqt.utils import showWarning

from .modify_notes import fill_field_for_note_in_editor, fill_field_for_note_not_in_editor
from .data_request import create_prompt, send_prompt_to_openai
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QPushButton
from PyQt5.QtCore import Qt
from concurrent.futures import Future, ThreadPoolExecutor
from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    progress_made = pyqtSignal(int)

    def __init__(self, notes, browser, prompt_config):
        super().__init__()
        self.notes = notes
        self.browser = browser
        self.prompt_config = prompt_config

    def run(self):
        for i, nid in enumerate(self.notes):
            if self.isInterruptionRequested():
                break
            if len(self.notes) == 1 and self.browser.editor and self.browser.editor.note:
                generate_for_single_note(self.browser.editor, self.prompt_config)
            else:
                generate_for_multiple_notes(nid, self.prompt_config)
            self.progress_made.emit(i)

class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Processing...')
        self.setWindowModality(Qt.ApplicationModal)
        self.progress_bar = QProgressBar(self)
        self.cancel_button = QPushButton('Cancel', self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.cancel_button)

        self.cancel_button.clicked.connect(self.cancel)
        self.worker = None

    def run_task(self, notes, prompt_config):
        self.progress_bar.setMaximum(len(notes))
        self.progress_bar.setValue(0)
        self.worker = Worker(notes, mw.col, prompt_config)  # pass the notes and prompt_config
        self.worker.progress_made.connect(self.update_progress)
        self.worker.start()
        self.show()

    def cancel(self):
        if self.worker:
            self.worker.requestInterruption()
        self.close()

    def update_progress(self, i):
        self.progress_bar.setValue(i + 1)
        if self.progress_bar.value() == self.progress_bar.maximum():
            self.close()


def generate_for_single_note(editor, prompt_config):
    """Generate text for a single note (editor note)."""
    prompt = create_prompt(editor.note, prompt_config)
    response = send_prompt_to_openai(prompt)

    target_field = prompt_config['targetField']
    fill_field_for_note_in_editor(response, target_field, editor)


def generate_for_multiple_notes(nid, prompt_config):
    """Generate text for multiple notes."""
    note = mw.col.get_note(nid)
    prompt = create_prompt(note, prompt_config)
    response = send_prompt_to_openai(prompt)
    fill_field_for_note_not_in_editor(response, note, prompt_config)



def process_notes(browser, prompt_config):
    selected_notes = browser.selectedNotes()
    if not selected_notes:
        showWarning("No notes selected.")
        return

    progress_dialog = ProgressDialog(browser)
    progress_dialog.run_task(selected_notes, prompt_config)  # pass selected_notes and prompt_config

