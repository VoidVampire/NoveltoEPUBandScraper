from bs4 import BeautifulSoup
import re
import json
import os
import glob
import shutil


def write_css_file():
    css_content = """body {
    margin: 2em; 
    padding: 0;
    font-family: serif;
    font-size: 1em; 
    line-height: 1.5; 
    text-align: justify; 
    hyphens: auto;
}

h1 {
    font-size: 1.8em; 
    text-align: center;
	font-weight: bold;
    margin: 0.5em;
}

.novel-title {
    font-size: 3em;
    margin-bottom: 0.5em;
}

.novel-details {
    font-size: 1.2em;
	text-align: center; 
}

#chapterName {
	margin-bottom: 1em;
}

h2 {
    font-size: 1.4em;
    text-align: center;
	font-weight: bold;
    margin: 0.5em 0;
}

h3 {
    font-size: 1.2em;
    font-weight: bold;
    margin: 1em 0 0.5em 0;
    text-align: left;
}

p {
    margin: 0 0 1em 0; 
    text-indent: 2em; 
}

blockquote {
    margin: 1em 2em;
    border-left: 5px solid #ccc;
    padding-left: 1em;
    font-style: italic;
}

hr {
    border: 1px;
    border-top: 2px solid;
    margin: 2em auto;
    width: 80%;
}

#title {
	margin: 1em auto;
	width: 25%;
}

em {
    font-style: italic;
}

strong {
    font-weight: bold;
}

img {
    display: block;
    margin: 1em auto;
    max-width: 100%; 
	max-height: 100%;
}

/* User Preference Support: Do not force anything */
:root {
    --font-family: serif;
    --font-size: 1em;
    --line-height: 1.5;
}

body {
    font-family: var(--font-family);
    font-size: var(--font-size);
    line-height: var(--line-height);
}"""

    css_path = os.path.join("output", "style.css")
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)
    print(f"Created style.css in output directory")


def create_toc_ncx(chapter_list, title="Novel Title"):
    # Create the navigation points
    nav_points = []
    for idx, chapter in enumerate(chapter_list, 1):
        # Format chapter number with leading zeros
        chapter_num = str(idx).zfill(3)
        # Escape special characters
        escaped_chapter = (
            chapter.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )

        nav_point = f"""    <navPoint id="navPoint-{idx}" playOrder="{idx}">
      <navLabel>
        <text>{escaped_chapter}</text>
      </navLabel>
      <content src="Text/chapter_{chapter_num}.xhtml"/>
    </navPoint>"""
        nav_points.append(nav_point)

    # Join all navigation points with newlines
    nav_content = "\n".join(nav_points)

    # Create the complete toc.ncx content
    escaped_title = (
        title.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
    toc_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
   "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:818be853-81bf-4b08-a14c-704bf57a6d81"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>{escaped_title}</text>
  </docTitle>
  <navMap>
{nav_content}
  </navMap>
</ncx>"""

    # Write the toc.ncx file to the processed_chapters directory
    toc_path = os.path.join("output", "toc.ncx")
    with open(toc_path, "w", encoding="utf-8") as f:
        f.write(toc_template)

    print("Created toc.ncx in processed_chapters directory")


def create_nav_file(chapter_list):
    # Create the navigation entries
    nav_entries = []

    for idx, chapter in enumerate(chapter_list, 1):
        # regex = r"Chapter \d+: (.+)"
        # match = re.search(regex, chapter)
        # chapter_name = match.group(1) if match else chapter
        chapter_num = str(idx-1).zfill(3)
        escaped_chapter = (
            chapter.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )
        nav_entries.append(
            f'    <li><a href="chapter_{chapter_num}.xhtml">{escaped_chapter}</a></li>'
        )

    # Join all navigation entries with newlines
    nav_content = "\n".join(nav_entries)

    # Create the complete nav.xhtml content
    nav_template = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
<head>
  <title>ePub NAV</title>
  <meta charset="utf-8"/>
  <link href="../Styles/style.css" rel="stylesheet" type="text/css"/>
</head>
<body epub:type="frontmatter">
  <nav epub:type="toc" id="toc" role="doc-toc"><h1 class="toc-title">Contents</h1>
  <ol class="chapter-list">
{nav_content}
  </ol></nav>
  <nav epub:type="landmarks" id="landmarks" hidden=""><h1>Landmarks</h1>
  <ol>
    <li><a epub:type="toc" href="#toc">Contents</a></li>
  </ol></nav>
</body>
</html>"""
    nav_template.replace("&", "&amp;")
    # Write the nav.xhtml file to the processed_chapters directory
    nav_path = os.path.join("output", "nav.xhtml")
    with open(nav_path, "w", encoding="utf-8") as f:
        f.write(nav_template)

    print("Created nav.xhtml in processed_chapters directory")


def create_cover(title):
    cover_template = f"""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>f{title}</title>
</head>
<body>
  <div style="text-align: center; padding: 0pt; margin: 0pt;">
    <svg xmlns="http://www.w3.org/2000/svg" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" viewBox="0 0 1200 1750" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink">
      <image width="1200" height="1750" xlink:href="../Images/cover.jpg"/>
    </svg>
  </div>
</body>
</html>
"""
    cover_path = os.path.join("output", "cover.xhtml")
    with open(cover_path, "w", encoding="utf-8") as f:
        f.write(cover_template)
    print("Created cover.xhtml in processed_chapters directory")


def create_cover_info(info):
    cover_template = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>{info[0]}</title>
  <link href="../Styles/style.css" rel="stylesheet" type="text/css"/>
</head>

<body>
  <div class="cover-container">
    <h1 class="novel-title">{info[0]}</h1>
    <h3 class="novel-details">{info[1]}</h3>
	<br/>
	<br/>
    <h3 class="novel-details">Translator: <span style="font-weight: normal;">{info[2]} @{info[3]}</span></h3>
  </div>
</body>
</html>"""
    cover_path = os.path.join("output", "coverpage.xhtml")
    with open(cover_path, "w", encoding="utf-8") as f:
        f.write(cover_template)
    print("Created coverpage.xhtml in processed_chapters directory")


def process_chapter(input_file, chapter_list):
    try:
        # Extract chapter number from filename
        chapter_file_num = re.search(r"chapter_(\d+)\.html", input_file).group(1)

        # Define output files with correct directory paths
        script_content_file = os.path.join(
            "script_contents", f"script_content_{chapter_file_num}.js"
        )
        json_output_file = os.path.join(
            "script_contents", f"chapter_{chapter_file_num}.json"
        )
        xhtml_output_file = os.path.join("output", f"chapter_{chapter_file_num}.xhtml")

        with open(input_file, "r", encoding="utf-8-sig") as file:
            html_doc = file.read()

        soup = BeautifulSoup(html_doc, "html.parser")
        soup.html.clear()
        script_tag = soup.find("script")

        # Save script content
        with open(script_content_file, "w", encoding="utf-8-sig") as script_file:
            data = script_tag.string.strip()
            script_file.write(data)
        print(f"Script content saved to '{script_content_file}'.")

        # Extract React query state
        match = re.search(r"window\.__REACT_QUERY_STATE__\s*=\s*({[\s\S]*?});", data)
        if not match:
            print(f"Could not find `window.__REACT_QUERY_STATE__` in {input_file}")
            return

        react_query_state = match.group(1)
        react_query_state = (
            react_query_state.replace("true", "True")
            .replace("false", "False")
            .replace("null", "None")
            .replace("undefined", "None")
        )
        try:
            react_query_state_dict = eval(react_query_state)
        except Exception as e:
            print(
                f"Failed to parse `window.__REACT_QUERY_STATE__` content in {input_file}: {e}"
            )
            return
        # Extract queries
        queries = react_query_state_dict.get("queries")
        if not queries or not isinstance(queries, list):
            print(f"No `queries` array found in the parsed data for {input_file}")
            return

        if len(queries) < 2:
            print(
                f"The `queries` array does not contain a second object in {input_file}"
            )
            return
        second_query = queries[1]["state"]["data"]["item"]["content"]["value"]
        chapter = queries[1]["state"]["data"]["item"]["name"]
        if chapter == "Prologue":
            chapter = "Chapter 0: Prologue"
        match = re.match(r"Chapter (\d+): (.+)", chapter)
        chapter_number = int(match.group(1))
        chapter_name = match.group(2)
        chapter_list.append(chapter)
        # Save JSON content
        try:
            with open(json_output_file, "w", encoding="utf-8-sig") as file:
                json.dump(second_query, file, indent=2, ensure_ascii=False)
            print(f"Extracted content saved to {json_output_file}")
        except Exception as e:
            print(f"Error writing to {json_output_file}: {e}")
            return

        # Process HTML content
        with open(json_output_file, "r", encoding="utf-8-sig") as file:
            data = file.read().strip()
            data = data[1:-1]

        soup = BeautifulSoup(data, "html.parser")
        for p_tag in soup.find_all("p"):
            p_tag.attrs = {}

        html_content = str(soup)
        html_content = (
            html_content.replace("<span>", "")
            .replace("</span>", "")
            .replace('\\"', "")
            .replace("\\n", "")
        )

        boilerplate = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
<title></title>
<link href="style.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<h1>{chapter_number}</h1>
<hr id="title"/>
<h2 id="chapterName">{chapter_name}</h2>
{html_content}
</body>
</html>
"""
        filled_xhtml = boilerplate.format(
            chapter_number=chapter_number,
            chapter_name=chapter_name,
            html_content=html_content,
        )

        # Save XHTML file
        with open(xhtml_output_file, "w", encoding="utf-8") as file:
            file.write(filled_xhtml)
        print(f"Created XHTML file: {xhtml_output_file}")
        return True

    except Exception as e:
        print(f"An error occurred processing {input_file}: {e}")
        return False


def main():
    # Create output directories if they don't exist
    os.makedirs("script_contents", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    chapter_list = []
    info = [
        "Book Name",
        "Author",
        "Translator",
        "Website",
    ]
    # Get all chapter HTML files
    input_directory = "html"
    chapter_files = sorted(glob.glob(os.path.join(input_directory, "chapter_*.html")))

    if not chapter_files:
        print(f"No chapter files found in {input_directory}")
        return

    print(f"Found {len(chapter_files)} chapter files to process")

    # Process each chapter file
    successful_chapters = 0
    for chapter_file in chapter_files:
        print(f"\nProcessing {chapter_file}...")
        if process_chapter(chapter_file, chapter_list):
            successful_chapters += 1

    print(
        f"\nProcessing completed. Successfully processed {successful_chapters} out of {len(chapter_files)} chapters."
    )

    # Clean up temporary files
    print("\nCleaning up temporary files...")
    if os.path.exists("script_contents"):
        shutil.rmtree("script_contents")
        print("Removed script_contents directory and all temporary files.")

    # Write CSS file
    write_css_file()
    create_nav_file(chapter_list)
    create_toc_ncx(chapter_list, info[0])
    create_cover(info[0])
    create_cover_info(info)
    print("\nAll processing completed!")


if __name__ == "__main__":
    main()
