from playwright.sync_api import sync_playwright

"""
Scroll down until the number of loaded media thumbnails stops increasing.
Kululu loads the media in a lazy way, so only the first thumbnails exists in the DOM initially
"""
def scroll_until_all_loaded(page):
    previous_count = -1

    while True:
        # Scroll down 3k pixels, timeout to load other media
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(500)

        count = page.locator("img[src*='thumbnail']").count()
        print(f"Loaded thumbnails: {count}")

        if count == previous_count:
            break

        previous_count = count

"""
Read the image or video URL from the currently visible Swiper (JS) slide.
Writes into unique_urls.txt:
media (image/video), URL
"""
def get_active_media(page):
    # Find HTML element that has a class of swiper-slide-active
    active = page.locator(".swiper-slide-active")

    # Then inside <video> element find <source>, which is the URL of the video
    source = active.locator("video source")
    if source.count() > 0:
        src = source.first.get_attribute("src")  # first selects the first <source> if there are multiple
        if src:
            return "video", src

    # Find <img> element that has an attribute of "preview"
    img = active.locator("img[alt='preview']")
    if img.count() > 0:
        src = img.first.get_attribute("src")
        if src:
            return "image", src

    # In case it goes wrong, return
    return None, None

def scrape_album(album_url, display_name, output_file, headless=False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=50)
        page = browser.new_page()

        print("Opening Kululu...")
        page.goto(album_url)
        page.locator("input").first.fill(display_name)
        page.locator("button").filter(has_text="Tęsti").click()

        # Wait 5 seconds for the img to appear
        page.locator("img[src*='thumbnail']").first.wait_for(timeout=5000)

        scroll_until_all_loaded(page)

        # Collects all the thumbnails that are loaded in the DOM after scrolling
        thumbs = page.locator("img[src*='thumbnail']")
        thumb_urls = []

        # Add unique URLs
        for i in range(thumbs.count()):
            src = thumbs.nth(i).get_attribute("src")
            if src and src not in thumb_urls:
                thumb_urls.append(src)

        # Add the function to check if the number matches the one shown on the Kululu
        print(f"\nUnique thumbnails found: {len(thumb_urls)}\n")

        # Collect media type and URL
        media = []

        for i, thumb_url in enumerate(thumb_urls, start=1):
            print(f"[{i}/{len(thumb_urls)}] Opening...")

            thumb = page.locator(f'img[src="{thumb_url}"]').first
            thumb.scroll_into_view_if_needed()
            page.wait_for_timeout(300)

            # Get thumbnail's coordinates and size
            box = thumb.bounding_box()
            if not box:
                print("  No bounding box")
                continue
            
            # Click the center of the thumbnail
            page.mouse.click(
                box["x"] + box["width"] / 2,
                box["y"] + box["height"] / 2
            )

            page.locator(".swiper-slide-active").wait_for(timeout=5000)
            page.wait_for_timeout(500)

            # Extract the type of media and URL
            media_type, url = get_active_media(page)

            if url:
                media.append((media_type, url))
                print(f"  {media_type}: {url}")
            else:
                print("  Could not find active media")

            page.keyboard.press("Escape")
            page.wait_for_timeout(500)

        # Removing duplicates
        unique = []
        seen = set()

        for media_type, url in media:
            if url not in seen:
                seen.add(url)
                unique.append((media_type, url))

        with open(output_file, "w", encoding="utf-8") as f:
            for media_type, url in unique:
                f.write(f"{media_type}\t{url}\n")

        print(f"\nCollected entries: {len(media)}")
        print(f"Unique URLs: {len(unique)}")
        print(f"Saved to {output_file}")

        browser.close()