import os
import requests
import time


def download_chapters(base_url, start_chapter, end_chapter):
    # Create the novel folder if it doesn't exist
    os.makedirs("html", exist_ok=True)

    # Download each chapter
    for chapter_num in range(start_chapter, end_chapter + 1):
        # Construct the full URL for the chapter
        url = f"{base_url}/chapter-{chapter_num}"

        try:
            # Send a GET request to fetch the HTML content
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Create the output filename with leading zeros for proper sorting
            output_file = os.path.join(
                "html", f"chapter_{chapter_num:03d}.html"
            )

            # Write the HTML content to a file
            with open(output_file, "w", encoding="utf-8-sig") as file:
                file.write(response.text)

            print(f"Downloaded chapter {chapter_num} to '{output_file}'.")

            # Add a small delay to avoid overwhelming the server
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Error downloading chapter {chapter_num}: {e}")
        except Exception as e:
            print(f"Unexpected error with chapter {chapter_num}: {e}")


# Base URL (replace with the actual base URL for the novel)
base_url = ""

# Download chapters 1-100
download_chapters(base_url, 0, 50)

print("Chapter download process completed.")
