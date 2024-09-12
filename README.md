# Simple Python scrapping a Wordpress - WooCommerce website

These scripts parse the content of Wordpress - Woocommerce / YOAST site.
More precisely, the generated sitemap.xml is loaded and parsed, and for each entry, the script navigate to the URLs and scrap multiple fields through Xpath.

## Scrapping Articles
This scripts parse a product-sitemap.xml, and for each entry, navigate to the URL and scrap useful elements such as the title, description, image url, image content, etc.
The images are stored in a Images root folder.
The data is registered into an Excel file.

The images are stored in a local folder ./images

## Scrapping Categories
This scripts parse a product_cat-sitemap.xml.xml, and for each entry, navigate to the URL and scrap the header and the footer.
The data is registered into an Excel file.

# Installation
Install the ChromeDriver on the local drive
```
python -m venv env
pip install selenium pandas markdownify
```
Create an "images" folder 

# Configuration
Put theses 3 values in the script : 
```
chrome_driver_path = "..." # Path to the local chrome driver
base_url = "..." # URL of the site to scrap
sitemap_url = "..." # URL containing all the URLs to scrap
```

# Author
Issam El Hachimi