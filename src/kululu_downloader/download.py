from pathlib import Path
from urllib.parse import urlparse
import requests

# ----------------------------
# Download folder
# ----------------------------

def download_media(urls_file, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)

    # ----------------------------
    # Read media URLs
    # ----------------------------

    media = []

    with open(urls_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            # unique_urls.txt contains: media_type<TAB>url
            _, url = line.split("\t", 1)
            media.append(url)

    print(f"Found {len(media)} files.\n")

    session = requests.Session()

    # ----------------------------
    # Download files
    # ----------------------------

    for i, url in enumerate(media, start=1):

        filename = Path(urlparse(url).path).name
        filepath = output_dir / filename

        if filepath.exists():
            print(f"[{i}/{len(media)}] Skipping {filename}")
            continue

        try:
            response = session.get(url, stream=True, timeout=30)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(64 * 1024):
                    if chunk:
                        f.write(chunk)

            print(f"[{i}/{len(media)}] Downloaded {filename}")

        except Exception as e:
            print(f"[{i}/{len(media)}] ERROR: {filename}")
            print(e)

    print("\nFinished!")
    print(f"Files saved to:\n{output_dir}")