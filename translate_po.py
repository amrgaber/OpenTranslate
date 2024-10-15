import os
import polib
from deep_translator import GoogleTranslator
import logging
import datetime

# Create a logger with a specific name (e.g., 'po_translator')
logger = logging.getLogger('po_translator')

# Set the logging level (e.g., 'INFO' for general information, 'DEBUG' for more details)
logger.setLevel(logging.INFO)

# Choose an output destination (e.g., console, file)
handler = logging.StreamHandler()
logger.addHandler(handler)

# Optionally, set a log format (e.g., timestamp, level, message)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


def get_user_input():
    src_path = input("Enter the path to the source PO file: ").strip()
    while not os.path.exists(src_path):
        print("File not found. Please try again.")
        src_path = input("Enter the path to the source PO file: ").strip()

    target_lang = input(
        "Enter the target language code (e.g., en, fr, es): ").strip()

    dest_dir = input(
        "Enter the destination directory for the translated file (press Enter for same as source): ").strip()
    if not dest_dir:
        dest_dir = os.path.dirname(src_path)

    return src_path, target_lang, dest_dir


def translate_po_file(src_path, target_lang, dest_dir):
    """
    Translates a PO file using Google Translate, replacing existing translations and avoiding new lines.

    Args:
        src_path: Path to the source PO file.
        target_lang: Target language code.
        dest_dir: Path to the destination directory.

    Returns:
        Path to the translated PO file.
    """

    # Handle relative paths based on current working directory:
    if not os.path.isabs(src_path):
        src_path = os.path.join(os.getcwd(), src_path)
        # Check if file exists
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"PO file not found at: {src_path}")
    if not os.access(src_path, os.R_OK):
        raise PermissionError(
            f"Insufficient permissions to access PO file: {src_path}")

    po = polib.pofile(src_path)
    for entry in po:  # Iterate over all entries (not just untranslated ones)
        if not entry.msgstr:  # Check if translation is missing
            translated_text = GoogleTranslator(
                source='auto', target=target_lang).translate(entry.msgid)
            entry.msgstr = translated_text  # Update the existing msgstr field

    # Determine destination directory
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Generate unique output file name using format string
    filename, ext = os.path.splitext(os.path.basename(src_path))
    short_filename = filename[:8]
    # Generate unique timestamp (6 digits for year and 2 digits for month)
    timestamp = datetime.datetime.now().strftime("%y%m_%H%M%S")
    new_filename = f"{short_filename}_{timestamp}.po"
    output_path = os.path.join(dest_dir, new_filename)
    po.save(output_path)
    return output_path


def main():
    logger.info("Starting PO translation script.")
    src_path, target_lang, dest_dir = get_user_input()
    logger.info(f"Source file: {src_path}")
    logger.info(f"Target language: {target_lang}")
    logger.info(f"Destination directory: {dest_dir}")

    translated_path = translate_po_file(src_path, target_lang, dest_dir)
    logger.info(f"Translated file saved to: {translated_path}")


if __name__ == "__main__":
    main()
