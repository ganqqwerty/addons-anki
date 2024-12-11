# IntelliFiller

## Development Setup
1. Clone the repository
2. Run `python scripts/setup_vendor.py` to install dependencies for your platform
   - For M1/M2 Mac users: Make sure you're running Python for ARM64
   - For Windows/Intel Mac users: The script will automatically handle your architecture

## Creating a Release
1. Run `python scripts/build_release.py` to build dependencies for all platforms
2. This will create platform-specific directories in the vendor folder:
   - darwin_arm64 (M1/M2 Macs)
   - darwin_x86_64 (Intel Macs)
   - win32 (Windows)
   - linux (Linux)
3. The add-on is now ready to be packaged and uploaded to AnkiWeb

## Troubleshooting
If you encounter architecture-related errors during development:
- M1/M2 Mac users: Ensure you're using the ARM64 version of Python
- Intel Mac users: Use the x86_64 version of Python