import subprocess
import shutil
import os
import platform
import sys

def build_all_platforms():
    # Get path to vendor directory
    vendor_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'IntelliFiller', 'vendor')
    
    # Clean/create vendor directory
    if os.path.exists(vendor_dir):
        shutil.rmtree(vendor_dir)
    os.makedirs(vendor_dir)

    platforms = [
        ('macosx_11_0_arm64', 'darwin_arm64'),
        ('macosx_10_15_x86_64', 'darwin_x86_64'),
        ('win_amd64', 'win32'),
        ('manylinux2014_x86_64', 'linux')
    ]
    
    for platform_tag, dir_name in platforms:
        platform_dir = os.path.join(vendor_dir, dir_name)
        os.makedirs(platform_dir, exist_ok=True)
        
        print(f"Building for {platform_tag}...")
        subprocess.check_call([
            'pip', 'install',
            '--platform', platform_tag,
            '--target', platform_dir,
            '--only-binary=:all:',
            'openai>=1.0.0',
            'httpx>=0.24.0'
        ])

if __name__ == '__main__':
    build_all_platforms()