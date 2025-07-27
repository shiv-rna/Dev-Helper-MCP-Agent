import os
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv

load_dotenv()

class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY in environment variables.")
        self.app = FirecrawlApp(api_key=api_key)

    def search_company(self, query: str, num_results: int = 5):
        try:
            result = self.app.search(
                query = f"{query} company pricing",
                limit = num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"]
                )
            )
            return result
        except Exception as e:
            print(f"An error occurred while searching for the company: {e}")
            return []

    def scrape_company_page(self, url: str):
        try:
            result = self.app.scrape_url(
                url=url,
                formats=["markdown"]
            )
            return result
        except Exception as e:
            print(f"An error occurred while scraping the company page: {e}")
            return None