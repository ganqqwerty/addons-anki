# -*- coding: utf-8 -*-

import os

from PyQt5.QtWidgets import QAction, QDialog, QVBoxLayout, QPushButton, QTextEdit
from aqt import mw
from anki.hooks import addHook
import json

addon_dir = os.path.dirname(os.path.realpath(__file__))
db_file = os.path.join(addon_dir, "kanji.json")
# Load the kanji data from the JSON file
with open(db_file, "r", encoding="utf-8") as file:
    KANJI_DATA = json.load(file)


def classify_kanji_by_jlpt(kanji_dict):
    jlpt_lists = {5: [], 4: [], 3: [], 2: [], 1: [], 'not_in_jlpt': []}

    for kanji, count in kanji_dict.items():
        if kanji in KANJI_DATA and "jlpt_new" in KANJI_DATA[kanji]:
            jlpt_level = KANJI_DATA[kanji]["jlpt_new"]
            if jlpt_level:  # Check if the level is not None
                jlpt_lists[jlpt_level].append((kanji, count))
            else:
                jlpt_lists['not_in_jlpt'].append((kanji, count))
        else:
            jlpt_lists['not_in_jlpt'].append((kanji, count))

    # Sort each JLPT list by count
    for level, kanji_list in jlpt_lists.items():
        jlpt_lists[level] = sorted(kanji_list, key=lambda item: item[1], reverse=True)

    return jlpt_lists[5], jlpt_lists[4], jlpt_lists[3], jlpt_lists[2], jlpt_lists[1], jlpt_lists['not_in_jlpt']


def get_kanji_count_by_note(cards, field_name):
    kanji_dict = {}
    no_field_count = 0

    for card_id in cards:
        card = mw.col.getCard(card_id)
        note = card.note()

        if field_name not in note:
            no_field_count += 1
            continue

        for char in note[field_name]:
            if is_kanji(char):
                kanji_dict[char] = kanji_dict.get(char, 0) + 1

    return kanji_dict, no_field_count


def get_sorted_list(kanji_dict, criteria_set):
    filtered_items = {k: v for k, v in kanji_dict.items() if k in criteria_set}.items()
    return sorted(filtered_items, key=lambda item: item[1], reverse=True)


def generate_kanji_table(jlpt_list):
    # Start the HTML table
    table_html = '<table border="1">'

    # Headers
    table_html += """
    <thead>
        <tr>
            <th>Kanji</th>
            <th>Onyomi</th>
            <th>Kunyomi</th>
            <th>Translations</th>
            <th>Popularity</th>
            <th>Amount</th> <!-- New column header -->
        </tr>
    </thead>
    <tbody>
    """

    for kanji, count in jlpt_list:
        data = KANJI_DATA.get(kanji, {})
        onyomi = ", ".join(data.get("readings_on", []))
        kunyomi = ", ".join(data.get("readings_kun", []))
        meanings = ", ".join(data.get("meanings", []))
        freq = data.get("freq", None)
        popularity = f"Top {freq}" if freq else ""

        table_html += f"""
        <tr>
            <td style="font-size: 24px;">{kanji}</td>
            <td>{onyomi}</td>
            <td>{kunyomi}</td>
            <td>{meanings}</td>
            <td>{popularity}</td>
            <td>{count}</td> <!-- New column data -->
        </tr>
        """

    # Close the table
    table_html += "</tbody></table>"

    return table_html


def format_kanji_statistics(kanji_dict, jlpt_lists, total_cards, no_field_count, kanji_count, kana_count, field_name):
    n5_list, n4_list, n3_list, n2_list, n1_list, not_in_jlpt = jlpt_lists

    CSS_STYLE = """
<style>
    table {
        border-collapse: collapse;
        width: 100%;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    th, td {
        border: 1px solid #d4d4d4;
        padding: 8px 12px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
    }
    tr:hover {
        background-color: #f5f5f5;
    }
</style>
"""

    stats = f"""{CSS_STYLE}
    <ul>
        <li>Total cards: {total_cards}</li>
        <li>Cards that don't have the "{field_name}" field: {no_field_count}</li>
        <li>Total japanese characters in "{field_name}" field: {kanji_count + kana_count}</li>
        <li>Kanji: {kanji_count}</li>
        <li>Unique kanji: {len(kanji_dict)}</li>
        <li>Kana: {kana_count}</li>
    </ul>
    <h3>N5 Kanji</h3>
    {generate_kanji_table(n5_list)}
    <h3>N4 Kanji</h3>
    {generate_kanji_table(n4_list)}
    <h3>N3 Kanji</h3>
    {generate_kanji_table(n3_list)}
    <h3>N2 Kanji</h3>
    {generate_kanji_table(n2_list)}
    <h3>N1 Kanji</h3>
    {generate_kanji_table(n1_list)}
    <h3>Not in JLPT</h3>
    {generate_kanji_table(not_in_jlpt)}"""

    return stats


def on_browser_init(browser):
    action = QAction("Count characters", browser)
    action.triggered.connect(lambda _, b=browser: show_dialog(b))
    browser.form.menuEdit.addAction(action)


addHook("browser.setupMenus", on_browser_init)


# Helper function to check if a character is Kanji
def is_kanji(ch):
    return 0x4E00 <= ord(ch) <= 0x9FFF


# Helper function to check if a character is Kana
def is_kana(ch):
    return (0x3040 <= ord(ch) <= 0x309F) or (0x30A0 <= ord(ch) <= 0x30FF)


def count_characters(cards, field_name):
    total_cards = len(cards)
    no_field_count = 0
    kanji_count = 0
    unique_kanji = set()
    kana_count = 0

    for card_id in cards:
        card = mw.col.getCard(card_id)
        note = card.note()
        if field_name in note:
            for char in note[field_name]:
                if is_kanji(char):
                    kanji_count += 1
                    unique_kanji.add(char)
                elif is_kana(char):
                    kana_count += 1
        else:
            no_field_count += 1

    kanji_dict, no_field_count = get_kanji_count_by_note(cards, field_name)
    jlpt_lists = classify_kanji_by_jlpt(kanji_dict)
    stats = format_kanji_statistics(kanji_dict, jlpt_lists, total_cards, no_field_count, kanji_count, kana_count,
                                    field_name)

    return stats


def add_context_menu_items(browser, menu):
    config = mw.addonManager.getConfig(__name__)

    action = QAction("Count characters", browser)
    action.triggered.connect(lambda _, b=browser: show_dialog(b))
    menu.addAction(action)


def show_dialog(browser):
    cards = browser.selected_cards()
    if not cards:
        return

    config = mw.addonManager.getConfig(__name__)
    default_field_name = config.get("default_field_name", "Your Field Name Here")

    dialog = QDialog(browser)
    dialog.setWindowTitle("Count Characters")

    layout = QVBoxLayout()

    field_name_input = QTextEdit()
    field_name_input.setPlainText(default_field_name)
    count_button = QPushButton("Count")
    result_display = QTextEdit()

    def on_count():
        field_name = field_name_input.toPlainText()
        stats = count_characters(cards, field_name)
        result_display.setHtml(stats)

    count_button.clicked.connect(on_count)

    layout.addWidget(field_name_input)
    layout.addWidget(count_button)
    layout.addWidget(result_display)

    dialog.setLayout(layout)
    dialog.exec_()


addHook("browser.onContextMenu", add_context_menu_items)
