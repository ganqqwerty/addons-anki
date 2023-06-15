import re
import os
import sys
from aqt.utils import showWarning
from aqt import mw

addon_dir = os.path.dirname(os.path.realpath(__file__))
vendor_dir = os.path.join(addon_dir, "vendor")
sys.path.append(vendor_dir)
import openai



from html import unescape


def create_prompt(note, prompt_config):
    prompt_template = prompt_config['prompt']
    pattern = re.compile(r'\{\{\{(\w+)\}\}\}')
    field_names = pattern.findall(prompt_template)
    for field_name in field_names:
        if field_name not in note:
            raise ValueError(f"Field '{field_name}' not found in note.")
        prompt_template = prompt_template.replace(f'{{{{{{{field_name}}}}}}}', note[field_name])
    # unescape HTML entities and replace line breaks with spaces
    prompt_template = unescape(prompt_template)
    # remove HTML tags
    prompt_template = re.sub('<.*?>', '', prompt_template)
    return prompt_template


def send_prompt_to_openai(prompt):
    config = mw.addonManager.getConfig(__name__)
    if config['emulate'] == 'yes':
        print("Fake request chatgpt: ", prompt)
        return f"This is a fake response for emulation mode for the prompt {prompt}."

    try:
        print("Request to ChatGPT: ", prompt)
        openai.api_key = config['apiKey']
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=2000)
        print("Response from ChatGPT", response)
        return response.choices[0].message.content.strip()

    except Exception as e:
        showWarning(f"An error occurred while processing the note: {str(e)}")
        return None
