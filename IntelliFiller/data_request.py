import re
import sys
import os
from aqt.utils import showWarning
from aqt import mw

import platform
def get_platform_specific_vendor():
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == 'darwin':  # macOS
        if machine == 'arm64':
            return 'darwin_arm64'
        return 'darwin_x86_64'
    elif system == 'windows':
        return 'win32'
    elif system == 'linux':
        return 'linux'
    else:
        raise RuntimeError(f"Unsupported platform: {system} {machine}")

addon_dir = os.path.dirname(os.path.realpath(__file__))
vendor_dir = os.path.join(addon_dir, "vendor", get_platform_specific_vendor())
sys.path.append(vendor_dir)

import openai
from .anthropic_client import SimpleAnthropicClient
import time;


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


def send_prompt_to_llm(prompt):
    config = mw.addonManager.getConfig(__name__)
    if config['emulate'] == 'yes':
        print("Fake request: ", prompt)
        return f"This is a fake response for emulation mode for the prompt {prompt}."

    try:
        print("Request to API: ", prompt)
        
        def try_openai_call():
            openai.api_key = config['apiKey']
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini", 
                messages=[{"role": "user", "content": prompt}], 
                max_tokens=2000
            )
            print("Response from OpenAI:", response)
            return response.choices[0].message.content.strip()
            
        def try_anthropic_call():
            client = SimpleAnthropicClient(api_key=config['anthropicKey'])
            response = client.create_message(prompt)
            print("Response from Anthropic:", response)
            return response

        maximum = 300
        while maximum > 0:
            maximum -= 1
            try:
                if config['selectedApi'] == 'anthropic':
                    return try_anthropic_call()
                else:  # openai
                    return try_openai_call()
            except openai.error.RateLimitError as e:
                time.sleep(1.0)  # Wait before retrying
            except Exception as e:
                # For other exceptions, we don't want to retry
                raise e

    except Exception as e:
        print(f"An error occurred while processing the note: {str(e)}", file=sys.stderr)
        showWarning(f"An error occurred while processing the note: {str(e)}")
        return None