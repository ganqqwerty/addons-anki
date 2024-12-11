import subprocess
import shutil
import os

def setup_vendor():
    # Create/clean vendor directory
    vendor_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'IntelliFiller', 'vendor')
    if os.path.exists(vendor_dir):
        shutil.rmtree(vendor_dir)
    os.makedirs(vendor_dir)

    # Install dependencies into vendor directory
    subprocess.check_call([
        'pip', 'install',
        '--target', vendor_dir,
        'openai>=1.0.0',
        'httpx>=0.24.0'
    ])

    # Remove unnecessary files to keep vendor directory slim
    for root, dirs, files in os.walk(vendor_dir):
        for dir_name in dirs:
            if dir_name in {'tests', 'test', '__pycache__', '*.dist-info'}:
                shutil.rmtree(os.path.join(root, dir_name))

if __name__ == '__main__':
    setup_vendor()