import argparse
import datetime
import os
import polib
from deep_translator import GoogleTranslator
import logging

# Create a logger with a specific name (e.g., 'po_translator')
logger = logging.getLogger('po_translator')

# Set the logging level (e.g., 'INFO' for general information, 'DEBUG' for more details)
logger.setLevel(logging.INFO)

# Choose an output destination (e.g., console, file)
# Option 1: Print to console
handler = logging.StreamHandler()
logger.addHandler(handler)

# Option 2: Write to a log file
# handler = logging.FileHandler('po_translator.log')
# logger.addHandler(handler)

# Optionally, set a log format (e.g., timestamp, level, message)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Translate PO files using Google Translate.")

    # Handle both relative and absolute paths with optional sub-folder:
    parser.add_argument("-p", "--path", required=True, help="Path to the source PO file (can be relative or absolute, may include sub-folder).")

    # Other arguments:
    parser.add_argument("-l", "--lang", required=True,
                        help="Target language code (e.g., en, fr, es) (required).")
    parser.add_argument("-d", "--dest_dir", default=None,
                        help="Destination directory for translated PO file (default: same directory as source if not specified).")
    parser.add_argument("-c", "--create_dir", action="store_true", default=False,
                        help="Create destination directory if it doesn't exist (only if -d is not specified).")
    parser.add_argument("-o", "--out_format", default="{base_name}_{date}_{time}.po",
                        help="Format string for generating the output file name (default: '%(base_name)s_%(date)s_%(time)s.po').")

    return parser.parse_args()

def translate_po_file(src_path, target_lang, dest_dir=None, create_dir=False, out_format="{base_name}_{date}_{time}.po"):
    """
    Translates a PO file using Google Translate, replacing existing translations and avoiding new lines.

    Args:
        src_path: Path to the source PO file.
        target_lang: Target language code.
        dest_path: Path to the destination PO file (optional, defaults to overwriting source).

    Returns:
        Path to the translated PO file.
    """

    # Handle relative paths based on current working directory:
    print(src_path)
    if not os.path.isabs(src_path):
        src_path = os.path.join(os.getcwd(), src_path)
        # Check if file exists
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"PO file not found at: {src_path}")
    if not os.access(src_path, os.R_OK):
        raise PermissionError(f"Insufficient permissions to access PO file: {src_path}")

    po = polib.pofile(src_path)
    for entry in po:  # Iterate over all entries (not just untranslated ones)
        if not entry.msgstr:  # Check if translation is missing
            translated_text = GoogleTranslator(source='auto', target=target_lang).translate(entry.msgid)
            entry.msgstr = translated_text  # Update the existing msgstr field

    # Determine destination directory
    if not dest_dir:
        dest_dir = os.path.dirname(src_path)  # Same directory as source

    # Ensure destination directory exists (only if not explicitly provided)
    if not os.path.exists(dest_dir) and not create_dir and not dest_dir:
        raise Exception(f"Destination directory '{dest_dir}' does not exist. Use -c to create it or specify a different -d option.")

    if not os.path.exists(dest_dir) and create_dir:
        os.makedirs(dest_dir)

    # Generate unique output file name using format string
    filename, ext = os.path.splitext(os.path.basename(src_path))
    short_filename = filename[:8]
    # Generate unique timestamp (6 digits for year and 2 digits for month)
    timestamp = datetime.datetime.now().strftime("%y%m_%H%M%S")
    new_filename = f"{short_filename}_{timestamp}.po"
    output_path = os.path.join(dest_dir, new_filename)
    po.save(output_path)
    print(f"Translated PO file saved to: {output_path}")

    return output_path

def main():
    args = parse_arguments()
    src_path = args.path
    target_lang = args.lang
    dest_dir = args.dest_dir
    create_dir = args.create_dir
    logger.info("Starting PO translation script.")
    logger.info(f"Source file: {src_path}")
    translated_path = translate_po_file(src_path, target_lang, dest_dir, create_dir, args.out_format)

if __name__ == "__main__":
    main()
