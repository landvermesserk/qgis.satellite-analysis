from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

# Enter your Copernicus Data Space credentials
USERNAME = "your_username"
PASSWORD = "your_password"

# Connect to the API
api = SentinelAPI(USERNAME, PASSWORD, "https://apihub.dataspace.copernicus.eu")

# Define the area of interest (GeoJSON or bounding box)
footprint = "POLYGON((lon1 lat1, lon2 lat1, lon2 lat2, lon1 lat2, lon1 lat1))"

# Search for Sentinel-2 images in the last 10 days
products = api.query(footprint,
                     date=('NOW-10DAYS', 'NOW'),
                     platformname='Sentinel-2',
                     cloudcoverpercentage=(0, 10))

# Download all found images
api.download_all(products)
