import os
from pathlib import Path
from OpenTranslate.translate_po import translate_po_file

# Path to the source and destination directories
SOURCE_DIR = Path('filesPO')
DEST_DIR = Path('FilesPoTranslate')

def get_po_files(source_dir):
    """
    Recursively find all .po files in the given directory.
    """
    return list(source_dir.rglob('*.po'))

def generate_output_filename(input_path):
    """
    Generate the output filename by appending ' - ar_001.po' before the extension.
    """
    parent = input_path.parent
    stem = input_path.stem
    return parent, f"{stem} - ar_001.po"

def main():
    # Ensure the destination directory exists
    DEST_DIR.mkdir(exist_ok=True)
    
    # Get all .po files
    po_files = get_po_files(SOURCE_DIR)
    if not po_files:
        print("No .po files found.")
        return
    
    print(f"Found {len(po_files)} .po files to translate")
    
    # Process all files
    for file_index, po_file in enumerate(po_files, 1):
        parent, output_filename = generate_output_filename(po_file.relative_to(SOURCE_DIR))
        output_dir = DEST_DIR / parent
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / output_filename

        print(f"[{file_index}/{len(po_files)}] Translating: {po_file} -> {output_path}")
        try:
            translate_po_file(
                src_path=str(po_file),
                target_lang='ar',
                output_path=str(output_path)
            )
            print(f"✓ Successfully translated: {output_filename}")
        except Exception as e:
            print(f"✗ Error translating {po_file}: {str(e)}")
    
    print("\nTranslation complete! All files processed.")

if __name__ == "__main__":
    main() 