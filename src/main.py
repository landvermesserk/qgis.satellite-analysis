import os
from datetime import date, timedelta
from copernicus_client import CopernicusAuth, SentinelImageRetriever

if __name__ == "__main__":
    # Retrieve credentials from environment variables
    USERNAME = os.getenv("COPERNICUS_USERNAME", "your_username")
    PASSWORD = os.getenv("COPERNICUS_PASSWORD", "your_password")

    # Define region of interest (modify coordinates as needed)
    FOOTPRINT = "POLYGON((-5 40, -5 41, -4 41, -4 40, -5 40))"

    # Define date range
    START_DATE = (date.today() - timedelta(days=10)).strftime("%Y-%m-%d")
    END_DATE = date.today().strftime("%Y-%m-%d")

    # Authenticate and retrieve API instance
    auth = CopernicusAuth(USERNAME, PASSWORD)
    api = auth.authenticate()

    if api:
        retriever = SentinelImageRetriever(api)
        products = retriever.search_images(FOOTPRINT, START_DATE, END_DATE)
        retriever.download_images(products)
