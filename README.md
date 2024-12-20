# Scraper and EPUB Creator

This project automates the process of scraping HTML chapters of a web novel website and converting them into an EPUB format for easy reading. It consists of two scripts:

1. `scraper.py`: Downloads chapters from the web.
2. `epubMaker.py`: Processes the downloaded HTML files and generates an files to be used in Sigil

## Features

### Scraper (`scraper.py`)
- Downloads chapters of a novel from a specified base URL.
- Organizes chapters into a `html/` directory for further processing.
- Configurable start and end chapter numbers.

### EPUB Maker (`epubMaker.py`)
- Converts HTML chapters into structured EPUB files.
- Generates a table of contents, stylesheet, and a cover.
- Cleans and processes chapter content for consistent formatting.

## Usage

### Step 1: Download Chapters
1. Set the `base_url` in `scraper.py` to the novel's base URL.
2. Configure the start and end chapter numbers.
3. Run the script:
   ```bash
   python scraper.py
   ```
   This will download chapters into the `html/` directory.

### Step 2: Generate EPUB
1. Place all HTML files in the `html/` directory.
2. Customize novel details in the `info` list within `epubMaker.py`.
3. Run the script:
   ```bash
   python epubMaker.py
   ```
   The EPUB components and files will be generated in the `output/` directory.

### Step 3: Finalize EPUB Using Sigil
1. Open Sigil and create a new EPUB (3.0).
2. Go to `File > Add > Add Existing Files` and:
   - Add all chapter files (`chapter_xxx.xhtml`) from the `output` directory.
   - Add the novel cover, renaming it to `cover.jpg`.
   - Delete the default `Section001.xhtml`.
3. Replace the contents of `nav.xhtml` in Sigil with the `nav.xhtml` generated in the `output` directory. If, for some reason, one wants to use EPUB 2.0 use the toc.ncx generated in output directory.
4. Replace the contents of the existing stylesheet in Sigil with the `style.css` file from the `output` directory, and rename it to `style.css`.
5. Open the Metadata Editor in Sigil and add relevant details such as:
   - Novel name
   - Author
   - Date published
   - Other optional metadata
6. Ensure that the files in the **Book Browser's "Text" section** are ordered correctly:
   - `cover.xhtml`
   - `nav.xhtml`
   - Chapter files (`chapter_xxx.xhtml` in sequential order).

Once completed,save your EPUB.
