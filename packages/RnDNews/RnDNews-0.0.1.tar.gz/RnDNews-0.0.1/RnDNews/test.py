from RnDNews.Shared_Methods import SharedMethods
from RnDNews.config import company_names, folder_path, zip_filename, MINIO_HOST, MINIO_PORT, MINIO_ACCESS_KEY, \
    MINIO_SECRET_KEY, MINIO_BUCKET
from RnDNews.DuckDuckGo_Scraper import DuckDuckGoScraper
from RnDNews.Google_Scraper import GoogleScraper
from RnDNews.Scraper import ScraperClient

if __name__ == "__main__":
    google_scraper = GoogleScraper()
    duckduckgo_scraper = DuckDuckGoScraper()

    client = ScraperClient(google_scraper)
    client.scrape(company_names)

    SharedMethods.zip_and_upload_to_minio(folder_path, zip_filename, MINIO_HOST, MINIO_PORT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY,
                            MINIO_BUCKET)

    #client.set_strategy(duckduckgo_scraper)
    #client.scrape(company_names[52:])




