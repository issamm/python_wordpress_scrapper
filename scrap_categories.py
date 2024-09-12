from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime

print(f"Début : {datetime.datetime.now()}")

chrome_driver_path = "C:/.../chromedriver-win64/chromedriver.exe"
base_url = "https://....com"
sitemap_url = "https://.../product_cat-sitemap.xml"

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(2) # seconds

crawled_links_list = []
already_visited_links_set = set()
all_categories = []


class Category:
    url = ""
    header = ""
    footer = ""

    def to_dict(self):
        return {
            'url' : self.url,
            'header' : self.header,
            'footer' : self.footer
        }
    
def scrape_website(base_url):
    driver.get(base_url)
    base_url = remove_lead_and_trail_slash_and_substring_to_sharp(base_url)
    put_all_links_into_the_set_of_links(base_url)
    already_visited_links_set.add(base_url)
    index = 0
    while index < len(crawled_links_list):
        subpage_url_to_scrap = crawled_links_list[index]
        index += 1
        scrape_single_page(subpage_url_to_scrap)

def put_all_links_into_the_set_of_links(url):
    article_links = driver.find_elements(By.CSS_SELECTOR, "a")
    num_links = len(article_links)
    nb_url_to_add_into_the_set = 0
    for i in range(num_links):
        subpage_link_element = article_links[i]
        subpage_link_url = subpage_link_element.get_attribute('href')
        if not subpage_link_url:
            continue
        if subpage_link_url == base_url:
            continue
        if not subpage_link_url.startswith(base_url):
            continue
        if "/product-categorie/" not in subpage_link_url:
            continue
        subpage_link_url = remove_lead_and_trail_slash_and_substring_to_sharp(subpage_link_url)
        if subpage_link_url not in already_visited_links_set:
            nb_url_to_add_into_the_set += 1
            crawled_links_list.append(subpage_link_url)
    print(f"Il y a {nb_url_to_add_into_the_set} liens sur la page : {url}, {len(crawled_links_list)} au total")

def remove_lead_and_trail_slash_and_substring_to_sharp(s):
    s = s.split('#')[0]
    if s.startswith('/'):
        s = s[1:]
    if s.endswith('/'):
        s = s[:-1]
    return s

def scrape_single_page(url):
    if not url:
        return
    if url in already_visited_links_set:
        return
    already_visited_links_set.add(url)
    driver.get(url)
    category = Category()
    category.url = url
    extract_from_subpage_field_header(category)
    extract_from_subpage_field_footer(category)
    all_categories.append(category)

def extract_from_subpage_field_header(category):
    try:
        header_xpath = '//div[@class="term-description"]'
        header_element = driver.find_elements(by=By.XPATH, value=header_xpath)
        if not header_element:
            return
        header_content = header_element[0].text
        category.header = header_content
    except Exception as e:
        return
    
def extract_from_subpage_field_footer(category):
    try:
        footer_xpath = '//div[@class="term-description et_second-description"]'
        footer_element = driver.find_elements(by=By.XPATH, value=footer_xpath)
        if not footer_element:
            return
        footer_content = footer_element[0].text
        category.footer = footer_content
    except Exception as e:
        return

scrape_website(sitemap_url)

print(f"{len(already_visited_links_set)} liens visités")

driver.quit()

### Construction du fichier XLSX

print(f"{len(all_categories)} catégories visités")

now = datetime.datetime.now()
if all_categories:
    from register_into_xlsx import *
    columns=[
        'url',
        'header',
        'footer'
    ]
    register(columns, all_categories, "categories")
print(f"Fin : {now}")
