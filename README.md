# kululu-downloader

A command-line tool that scrapes and downloads all photos and videos from a
[Kululu](https://kululu.com) event album — the kind of guest-upload photo
wall commonly used at weddings and parties.

Kululu sometimes doesn't provide a built-in "download all" option (depending 
on options selected by the album creator), so this tool drives
a real browser (via [Playwright](https://playwright.dev/python/)) to open
every photo and video in the album, read out its full-quality URL, and save
each file to your computer.

It works in two steps: `scrape` collects the media URLs from the album page,
and `download` fetches the actual files using that list.

## Installation

Install the tool directly from GitHub:

```bash
pip install git+https://github.com/JustGva/kululu-downloader.git
```

Then, download the browser Playwright needs to run the scraper:

```bash
playwright install chromium
```

That's it — you're ready to use `kululu-dl`. See [Usage](#usage) below.

## Usage

### 1. Scrape the album

Collect the media URLs from a Kululu album:

```bash
kululu-dl scrape "https://app.kululu.com/YourAlbumURL" --name "Your Name"
```

A browser window will open, enter the album using the display name you gave,
scroll to load every thumbnail, then click through each one to read its
full-quality URL. This can take a while for large albums — leave the window
alone while it runs.

By default, the results are saved to `unique_urls.txt` in your current
folder. You can change that with `--out`:

```bash
kululu-dl scrape "https://app.kululu.com/YourAlbumURL" --name "Your Name" --out my_album_urls.txt
```

Once you trust it's working correctly, you can add `--headless` to run
without a visible browser window:

```bash
kululu-dl scrape "https://app.kululu.com/YourAlbumURL" --name "Your Name" --headless
```

### 2. Download the files

```bash
kululu-dl download --out ./my-photos
```

This reads `unique_urls.txt` (the file `scrape` just created) and downloads
every file into the folder given by `--out`. Already-downloaded files are
skipped, so it's safe to re-run if something fails partway through.

If you used a custom filename in step 1, point to it with `--urls-file`:

```bash
kululu-dl download --urls-file my_album_urls.txt --out ./my-photos
```

## Notes

- This is an independent, unofficial tool and isn't affiliated with or
  endorsed by Kululu.
- Please use this tool if and only if you have the permission of the album owner. 

## License

MIT
