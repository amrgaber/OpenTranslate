OpenTranslate

Prerequisites:

- Python 3.x (https://www.python.org/)

Installation:

1. Clone the repository: git clone https://github.com/amrgaber/OpenTranslate.git
2. Install dependencies: pip install -r requirements.txt

Usage:

1. Run the script from the command line:

   python open_translate.py
2. Follow the prompts to enter:

   - The path to your source PO file (relative or absolute)
   - The desired target language code (e.g., ar, fr)
   - The destination directory for the translated file (optional, press Enter to use the same directory as the source file)

Example interaction:

Enter the path to the source PO file: my_translation.po
Enter the target language code (e.g., en, fr, es): ar
Enter the destination directory for the translated file (press Enter for same as source): localized_files

This translates my_translation.po into Arabic and saves the file with a unique timestamp (e.g., my_trans_2402_200000.po) in the localized_files directory. If the directory doesn't exist, it will be created automatically.

Features:

- Translates all entries in the PO file, not just untranslated ones
- Generates unique filenames with timestamps to prevent overwriting
- Creates the destination directory if it doesn't exist
- Provides logging information about the translation process

Note: This script uses the Google Translate API for translations. Make sure you comply with Google's terms of service when using this tool.
