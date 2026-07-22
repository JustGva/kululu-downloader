import argparse
from pathlib import Path
from kululu_downloader.download import download_media
from kululu_downloader.scrape import scrape_album

def main():
    parser = argparse.ArgumentParser(prog="kululu-dl")
    subparsers = parser.add_subparsers(dest="command", required=True)

    download_parser = subparsers.add_parser("download")
    download_parser.add_argument("--out", required=True, type=Path)
    download_parser.add_argument("--urls-file", required=False, default="unique_urls.txt")

    scrape_parser = subparsers.add_parser("scrape")
    scrape_parser.add_argument("album_url")
    scrape_parser.add_argument("--name", required=True)
    scrape_parser.add_argument("--out", default="unique_urls.txt")
    scrape_parser.add_argument("--headless", action="store_true")  # if --headless -> True, if skipped -> False

    args = parser.parse_args()

    if args.command == "download":
        download_media(urls_file=args.urls_file, output_dir=args.out)
    elif args.command == "scrape":
        scrape_album(album_url=args.album_url, display_name=args.name, output_file=args.out, headless=args.headless)
