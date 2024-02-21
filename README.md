# OpenTranslate


**Prerequisites:**

-   Python 3.x ([https://www.python.org/](https://www.python.org/))

**Installation:**

1.  **Clone the repository:** `git clone https://github.com/amrgaber/OpenTranslate.git`
2.  **Install dependencies:** `pip install -r requirements.txt` (if a requirements file exists)

**Usage:**

1.  Run the script from the command line:

Bash

```
python [script-name].py -p <source_file> -l <target_language> [options]

```

2.  Replace `<source_file>` with the path to your source PO file (relative or absolute).
    
3.  Replace `<target_language>` with the desired language code (e.g., `ar`, `fr`).
    
4.  Use optional arguments for customization:
    
    -   `-d`: Destination directory for the translated file (defaults to source directory).
    -   `-c`: Create destination directory if it doesn't exist.
    -   `-o`: Output filename format (default: `<base_name>_<date>_<time>.po`).

**Example:**

Bash

```
python translate_po.py -p my_translation.po -l ar -d localized_files

```

This translates `my_translations.po` into Arabic and saves the file as `my_translations_2402_200000.po` in the `localized_files` directory (if it exists, otherwise it's created).
