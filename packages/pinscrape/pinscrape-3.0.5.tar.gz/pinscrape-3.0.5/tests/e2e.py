from pinscrape import scraper


details = scraper.scrape("messi", "output", {}, 10, 15)


def test_single_data():
    if details["isDownloaded"]:
        print("\nDownloading completed !!")
        print(f"\nTotal urls found: {len(details['extracted_urls'])}")
        print(f"\nTotal images downloaded (including duplicate images): {len(details['url_list'])}")
        print(details)
    else:
        print("\nNothing to download !!")

    assert len(details['extracted_urls']) > 0
