import os
import logging
from typing import Optional, Dict, Tuple
from sentinelsat import SentinelAPI
from datetime import date, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class SentinelImageRetriever:
    """
    Searches and downloads Sentinel satellite images.
    """
    def __init__(self, api: SentinelAPI) -> None:
        self.api = api

    def search_images(
    footprint: str,
    start_date: str,
    end_date: str,
    cloud_cover: Tuple[int, int] = (0, 10),
) -> Dict:
        """
        Searches for Sentinel-2 images in a given region and date range.

        Description:
        This function queries the Copernicus Data Space API to find available 
        Sentinel-2 images within a specified geographical region and date range. 
        The function filters results based on cloud cover percentage to ensure 
        optimal image quality.

        Parameters:
        - footprint (str): A WKT (Well-Known Text) string defining the area of interest. 
        This should be a polygon or bounding box specifying the desired search region.
        - start_date (str): The beginning of the search period in "YYYY-MM-DD" format.
        - end_date (str): The end of the search period in "YYYY-MM-DD" format.
        - cloud_cover (Tuple[int, int], optional, default=(0, 10)): A tuple specifying 
        the minimum and maximum cloud cover percentage allowed (0-100%). Lower values 
        help obtain clearer images.

        Returns:
        - Dict: A dictionary containing metadata of the found Sentinel-2 products, 
        including product IDs, acquisition dates, cloud coverage, and download links.

        Example Usage:
        ```python
        products = retriever.search_images(
            footprint="POLYGON((-5 40, -5 41, -4 41, -4 40, -5 40))",
            start_date="2024-02-01",
            end_date="2024-02-10",
            cloud_cover=(0, 20)
        )
        print(f"Found {len(products)} images.")
        ```

        Notes:
        - Ensure that the provided footprint is in a valid WKT format.
        - Sentinel-2 images have a revisit time of approximately 5 days per location, 
        so adjust the date range accordingly.
        - The function requires an authenticated SentinelAPI instance to query the database.

        References:
        - Sentinelsat Documentation: https://sentinelsat.readthedocs.io/
        """
        try:
            products = self.api.query(
                footprint,
                date=(start_date, end_date),
                platformname="Sentinel-2",
                cloudcoverpercentage=cloud_cover,
            )
            logging.info(f"Found {len(products)} images.")
            return products
        except Exception as e:
            logging.error(f"Error searching images: {e}")
            return {}

    def download_images(self, products: Dict, download_dir: str = "downloads") -> None:
        """
        Downloads images from the retrieved product list.

        Parameters:
            products: Dictionary of Sentinel products to download.
            download_dir: Directory to save images.
        """
        if not products:
            logging.warning("No products found. Exiting download process.")
            return

        os.makedirs(download_dir, exist_ok=True)

        for product_id in products.keys():
            try:
                logging.info(f"⬇️ Downloading {product_id}...")
                self.api.download(product_id, directory_path=download_dir)
                logging.info(f"Downloaded: {product_id}")
            except Exception as e:
                logging.error(f"Error downloading {product_id}: {e}")