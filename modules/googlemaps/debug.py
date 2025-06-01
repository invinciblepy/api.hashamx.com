from scraper import googlemaps


def main():
    url = "https://www.google.com/maps/search/restaurants/@34.0387325,71.6079893,14z?entry=ttu&g_ep=EgoyMDI1MDUyOC4wIKXMDSoASAFQAw%3D%3D"
    scraper = googlemaps(url)
    print(scraper.scrape())

if __name__ == "__main__":
    main()