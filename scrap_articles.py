from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import markdownify
import urllib

import datetime

print(f"Début : {datetime.datetime.now()}")

chrome_driver_path = "C:/.../chromedriver-win64/chromedriver.exe"
base_url = "https://....com"
sitemap_url = "https://.../product-sitemap.xml"

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(1) # seconds

crawled_links_list = []
already_visited_links_set = set()
all_articles = []


class Article:
    url = ""
    is_article = False
    title = ""
    price = -1
    reducted_price = -1
    short_description = ""
    image_main_url = ""
    image_gallery_url = ""
    yoast_title = ""
    yoast_description = ""
    product_url = ""
    public_target_type = ""
    public_target_age = ""
    long_description = ""
    category = ""

    def to_dict(self):
        return {
            'url' : self.url,
            'title' : self.title,
            'price' : self.price,
            'reducted_price' : self.reducted_price,
            'short_description' : self.short_description,
            'image_main_url' : self.image_main_url,
            'image_gallery_url' : self.image_gallery_url,
            'yoast_title' : self.yoast_title,
            'yoast_description' : self.yoast_description,
            'product_url' : self.product_url,
            'public_target_type' : self.public_target_type,
            'public_target_age' : self.public_target_age,
            'long_description' : self.long_description,
            'category' : self.category,
            'og_title' : self.og_title,
            'og_description': self.og_description
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
        if "/product/" not in subpage_link_url:
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
    print(f"Navigation vers {url}")
    driver.get(url)

    article = Article()
    article.url = url
    extract_from_subpage_field_price(article)
    extract_from_subpage_field_product_title(article)
    extract_from_subpage_field_product_short_description(article)
    extract_from_subpage_field_product_category(article)
    extract_from_subpage_field_image_main_url(article)
    extract_from_subpage_field_image_gallery_url(article)
    extract_from_subpage_field_yoast_title(article)
    extract_from_subpage_field_yoast_description(article)
    extract_from_subpage_field_product_url(article)
    extract_from_subpage_field_public_target_type(article)
    extract_from_subpage_field_public_target_age(article)
    extract_from_subpage_field_long_description(article)
    extract_from_subpage_field_og_title(article)
    extract_from_subpage_field_og_description(article)
    all_articles.append(article)

def extract_from_subpage_field_price(article):
    try:
        price_xpath = '//div[@class="element-TFML4 et_column et_product-block mob-full-width mob-full-width-children justify-content-start"]//bdi'
        price_element = driver.find_elements(by=By.XPATH, value=price_xpath)
        if not price_element:
            return
        price = price_element[0].text
        article.price = price
        article.reducted_price = price
        article.is_article = True
        reducted_price = ''
        if price_element[1]:
            reducted_price = price_element[1].text
            article.reducted_price = reducted_price
    except Exception as e:
        return
    
def extract_from_subpage_field_product_title(article):
    try:
        product_title_xpath = '//h1[contains(@class, "product_title") and contains(@class, "entry-title")]'
        product_title_element = driver.find_elements(by=By.XPATH, value=product_title_xpath)
        if not product_title_element:
            return
        product_title = product_title_element[0].text
        article.title = product_title
    except Exception as e:
        return

def extract_from_subpage_field_product_short_description(article):
    try:
        product_short_description_xpath = '//div[@class="woocommerce-product-details__short-description"]'
        product_short_description_element = driver.find_elements(by=By.XPATH, value=product_short_description_xpath)
        if not product_short_description_element:
            return
        product_short_description = product_short_description_element[0].text
        article.short_description = product_short_description
    except Exception as e:
        return
    
def extract_from_subpage_field_product_category(article):
    try:
        product_category_xpath = '//span[@class="posted_in"]/a'
        product_category_element = driver.find_elements(by=By.XPATH, value=product_category_xpath)
        if not product_category_element:
            return
        product_category = product_category_element[0].text
        article.category = product_category
    except Exception as e:
        return

def extract_from_subpage_field_image_main_url(article):
    try:
        image_main_url_xpath = '//a[@class="woocommerce-main-image pswp-main-image zoom"]'
        image_main_url_element = driver.find_elements(by=By.XPATH, value=image_main_url_xpath)
        if not image_main_url_element:
            return
        image_main_url = image_main_url_element[0].get_attribute("href")
        article.image_main_url = image_main_url
        save_image_on_disk(image_main_url)
    except Exception as e:
        return

def extract_from_subpage_field_image_gallery_url(article):
    try:
        image_gallery_url_xpath = '//a[@class="woocommerce-main-image zoom"]'
        image_gallery_url_element = driver.find_elements(by=By.XPATH, value=image_gallery_url_xpath)
        if not image_gallery_url_element:
            return
        image_gallery_url = image_gallery_url_element[0].get_attribute("href")
        article.image_gallery_url = image_gallery_url
        save_image_on_disk(image_gallery_url)
    except Exception as e:
        return

def extract_from_subpage_field_yoast_title(article):
    try:
        yoast_title_xpath = '//title'
        yoast_title_element = driver.find_elements(by=By.XPATH, value=yoast_title_xpath)
        yoast_title = yoast_title_element[0].get_attribute("innerHTML")
        article.yoast_title = yoast_title
    except Exception as e:
        return

def extract_from_subpage_field_yoast_description(article):
    try:
        yoast_description_xpath = '//meta[@name="description"]'
        yoast_description_element = driver.find_elements(by=By.XPATH, value=yoast_description_xpath)
        yoast_description = yoast_description_element[0].get_attribute("content")
        article.yoast_description = yoast_description
    except Exception as e:
        return

def extract_from_subpage_field_product_url(article):
    try:
        product_url_xpath = '//div[@class="element-TFML4 et_column et_product-block mob-full-width mob-full-width-children justify-content-start"]/a'
        product_url_element = driver.find_elements(by=By.XPATH, value=product_url_xpath)
        product_url = product_url_element[0].get_attribute("href")
        article.product_url = product_url
    except Exception as e:
        return

def extract_from_subpage_field_public_target_type(article):
    try:
        public_target_type_xpath = '//tr[contains(@class, "woocommerce-product-attributes-item--attribute_pa_doelgroep")]/td/p'
        public_target_type_element = driver.find_elements(by=By.XPATH, value=public_target_type_xpath)
        public_target_type = public_target_type_element[0].get_attribute("innerHTML")
        article.public_target_type = public_target_type
    except Exception as e:
        return

def extract_from_subpage_field_public_target_age(article):
    try:
        public_target_age_xpath = '//tr[contains(@class, "woocommerce-product-attributes-item--attribute_pa_leeftijd")]/td/p'
        public_target_age_element = driver.find_elements(by=By.XPATH, value=public_target_age_xpath)
        public_target_age = public_target_age_element[0].get_attribute("innerHTML")
        article.public_target_age = public_target_age
    except Exception as e:
        return
    
def extract_from_subpage_field_long_description(article):
    try:
        long_description_xpath = '//div[contains(@class, "woocommerce-Tabs-panel--description")]'
        long_description_element = driver.find_elements(by=By.XPATH, value=long_description_xpath)
        long_description = long_description_element[0].get_attribute("innerHTML")
        long_description = markdownify.markdownify(long_description)
        article.long_description = long_description.strip()
    except Exception as e:
        return

def extract_from_subpage_field_og_title(article):
    try:
        og_title_xpath = '//meta[@property="og:title"]'
        og_title_element = driver.find_elements(by=By.XPATH, value=og_title_xpath)
        og_title = og_title_element[0].get_attribute("content")
        article.og_title = og_title.strip()
    except Exception as e:
        return

def extract_from_subpage_field_og_description(article):
    try:
        og_description_xpath = '//meta[@property="og:description"]'
        og_description_element = driver.find_elements(by=By.XPATH, value=og_description_xpath)
        og_description = og_description_element[0].get_attribute("content")
        article.og_description = og_description.strip()
    except Exception as e:
        return


import ssl
context = ssl._create_unverified_context()

def save_image_on_disk(url):

    image_filename = url.split('/')[-1]
    resource = urllib.request.urlopen(url, context=context)
    output = open("images/" + image_filename, "wb")
    output.write(resource.read())
    output.close()
    urllib.request.urlretrieve(url, image_filename)

scrape_website(sitemap_url)

print(f"{len(already_visited_links_set)} liens visités")

driver.quit()

### Construction du fichier XLSX

def has_price_filter(article):
    return article.is_article

print(f"{len(all_articles)} article visités")
articles_with_price = list(filter(has_price_filter, all_articles))
print(f"{len(articles_with_price)} article visités avec prix")



if articles_with_price:
    from register_into_xlsx import *
    columns=[
                                            'url',
                                            'title',
                                            'price',
                                            'reducted_price',
                                            'short_description',
                                            'image_main_url',
                                            'image_gallery_url',
                                            'yoast_title',
                                            'yoast_description',
                                            'product_url',
                                            'public_target_type',
                                            'public_target_age',
                                            'long_description',
                                            'category',
                                            'og_title',
                                            'og_description'
    ]
    register(columns, all_articles, "products")

print(f"Fin du traitement")
