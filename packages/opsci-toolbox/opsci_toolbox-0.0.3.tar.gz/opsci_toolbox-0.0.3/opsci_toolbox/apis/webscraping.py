from urllib.parse import urlparse
import requests
from trafilatura import extract
from bs4 import BeautifulSoup
from opsci_toolbox.helpers.common import write_json, read_json, list_files_in_dir, save_dataframe_csv
import justext
import os
import hashlib
import re
import concurrent.futures
import pandas as pd
from tqdm import tqdm


def url_get_domain(url):
    """
    Return the domain name from a url
    """
    parsed_url = urlparse(url)
    domain = parsed_url.hostname if parsed_url.hostname else parsed_url.netloc
    return domain


def url_get_extension(url):
    """
    Return the extension of the domain name from a url
    """
    # Parse the URL using urlparse
    parsed_url = urlparse(url)

    # Extract the netloc (network location) from the parsed URL
    netloc = parsed_url.netloc

    # Split the netloc by '.' to get the domain and TLD
    domain_parts = netloc.split(".")

    # Get the last two parts, which represent the domain and TLD
    extension = ".".join(domain_parts[-1:])

    return extension


def url_clean_parameters(url):
    """
    Return a URL without any parameters or utm tags
    """
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc if parsed_url.netloc else ""
    path = parsed_url.path if parsed_url.path else ""
    return netloc + path


def url_clean_protocol(url):
    """
    Remove https / http from a url
    """
    prefixes_to_remove = ["https://", "http://"]

    for prefix in prefixes_to_remove:
        if url.startswith(prefix):
            url = url[len(prefix) :]
            break

    return url


def url_remove_www(url):
    """
    Remove www from a url
    """
    prefixes_to_remove = ["https://www.", "http://www.", "https://", "http://", "www."]

    for prefix in prefixes_to_remove:
        if url.startswith(prefix):
            url = url[len(prefix) :]
            break

    return url


def url_add_protocol(url):
    """
    Return a formatted url with protocol and www. if necessary
    """
    parsed_url = urlparse(url)

    if len(parsed_url.scheme) < 1 and parsed_url.path.startswith("www"):
        url = "https://" + url
    elif len(parsed_url.scheme) < 1 and len(parsed_url.path.split(".")) < 3:
        url = "https://www." + url
    elif len(parsed_url.scheme) < 1 and len(parsed_url.path.split(".")) > 2:
        url = "https://" + url
    else:
        return url

    return url


def url_is_valid(url):
    """
    Checks if a URL is valid
    """
    try:
        parsed_url = urlparse(url)
        return parsed_url.scheme in ["http", "https"] and parsed_url.netloc != ""
    except Exception as e:
        # If there is any error during URL parsing, consider it invalid
        return False


def url_is_reachable(url):
    """
    Checks if url is reachable (no 404 error...)
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True  # No HTTP error, URL is reachable
    except requests.RequestException as e:
        print(f"Error: {e}")
        return False  # HTTP error occurred, URL is not reachable


def scrape(url):
    """
    Get requests and return full response
    """
    try:
        response = requests.get(url)
    except Exception as e:
        pass
        print(e, "-", url)
    return response


def justext_parse_content(response, languages=["English", "French"]):
    """
    Return main content from a HTML response
    """

    stoplist = frozenset()

    for lang in languages:
        current_stoplist = justext.get_stoplist(lang)
        stoplist = stoplist.union(current_stoplist)

    try:
        paragraphs = justext.justext(response.content, stoplist)
        filtered_paragraphs = [
            paragraph.text for paragraph in paragraphs if not paragraph.is_boilerplate
        ]
        concatenated_text = ". ".join(filtered_paragraphs)
        concatenated_text = re.sub(r"\.\. ", ". ", concatenated_text)

    except Exception as e:
        pass
        print(e)
    return concatenated_text


def trafilatura_parse_content(response):
    """
    Return main content from a HTML response
    """
    try:
        text = extract(response.content)
    except Exception as e:
        pass
        print(e)
    return text


def process_scraping(
    url,
    path,
    method="justext",
    languages=["English", "French"],
    title=True,
    meta=True,
    lst_properties=[
        "og:site_name",
        "og:url",
        "og:title",
        "og:description",
        "og:type",
        "og:article:section",
        "og:article:author",
        "og:article:published_time",
        "article:modified_time",
        "og:image",
        "og:image:width",
        "og:image:height",
        "og:video",
        "og:video:url",
        "og:video:width",
        "og:video:height",
        "fb:page_id",
        "twitter:url",
        "twitter:title",
        "twitter:description",
        "twitter:image",
        "al:ios:app_store_id",
        "al:ios:app_name",
        "al:android:package",
        "al:android:app_name",
    ],
):
    try:

        # We name the files
        data = dict()
        url_hash = hashlib.md5(url.encode()).hexdigest()
        filename = f"scraped_data_{url_hash}.json"
        filepath = os.path.join(path, filename)

        # we scrape the HTML page
        response = scrape(url)

        # we parse the response to get main content and eventually title and meta tags
        if method == "justext":
            text = justext_parse_content(response, languages)
        else:
            text = trafilatura_parse_content(response)

        # we create a dict with results
        data = {"path": filepath, "url": url}

        if text:
            data["text"] = text
        else:
            data["text"] = None

        if title:
            title_txt = parse_title(response)
            data["title"] = title_txt
        else:
            data["title"] = None

        if meta:
            meta_dict = get_meta_properties(response)
            for key in meta_dict.keys():
                data[key] = meta_dict[key]
        else:
            for key in lst_properties:
                data[key] = None

        # we store the json file
        if not os.path.exists(filepath):
            write_json(data, path, filename)
        else:
            data = read_json(filepath)

        return data

    except Exception as e:
        print(url, "-", e)
        return None


def parse_title(response):
    """
    Return webpage title
    """
    try:
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the title tag and extract its text
        title_tag = soup.find("title")
        if title_tag:
            return title_tag.text.strip()
        else:
            print("No title found")
            return None
    except Exception as e:
        pass
        print(e)
        return None


def get_meta_properties(
    response,
    lst_properties=[
        "og:site_name",
        "og:url",
        "og:title",
        "og:description",
        "og:type",
        "og:article:section",
        "og:article:author",
        "og:article:published_time",
        "article:modified_time",
        "og:image",
        "og:image:width",
        "og:image:height",
        "og:video",
        "og:video:url",
        "og:video:width",
        "og:video:height",
        "fb:page_id",
        "twitter:url",
        "twitter:title",
        "twitter:description",
        "twitter:image",
        "al:ios:app_store_id",
        "al:ios:app_name",
        "al:android:package",
        "al:android:app_name",
    ],
):
    """
    Parse a list of meta tags from a webpage and returns a dict
    """
    try:

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all 'meta' tags
        meta_tags = soup.find_all("meta")

        # Extract meta properties and content
        meta_properties = {}
        for meta_tag in meta_tags:
            property_attr = meta_tag.get("property")
            content_attr = meta_tag.get("content")

            if property_attr and content_attr:
                if property_attr in lst_properties:
                    meta_properties[property_attr] = content_attr
                else:
                    meta_properties[property_attr] = None

        return meta_properties

    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


def parallel_scraping(
    urls,
    path,
    max_workers=8,
    method="justext",
    languages=["English", "French"],
    title=True,
    meta=True,
    lst_properties=[
        "og:site_name",
        "og:url",
        "og:title",
        "og:description",
        "og:type",
        "og:article:section",
        "og:article:author",
        "og:article:published_time",
        "article:modified_time",
        "og:image",
        "og:image:width",
        "og:image:height",
        "og:video",
        "og:video:url",
        "og:video:width",
        "og:video:height",
        "fb:page_id",
        "twitter:url",
        "twitter:title",
        "twitter:description",
        "twitter:image",
        "al:ios:app_store_id",
        "al:ios:app_name",
        "al:android:package",
        "al:android:app_name",
    ],
):

    """
    Execute concurrent threads to scrape multiple webpages
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit scraping tasks for each URL and add tqdm progress bar
        futures = [
            executor.submit(
                process_scraping,
                url,
                path,
                method,
                languages,
                title,
                meta,
                lst_properties,
            )
            for url in urls
        ]
        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(urls),
            desc="Scraping Progress",
        ):
            try:
                data = future.result()
            except Exception as e:
                print(f"Error scraping : {e}")


def parse_scraped_webpages(path_json_files, output_path, name):
    """
    Parse JSON files captured by scraper
    """
    extracted_data = []

    files_to_parse = list_files_in_dir(path_json_files, "*.json")

    for file in tqdm(
        files_to_parse, total=len(files_to_parse), desc="Parsing files progress"
    ):
        data = read_json(file)
        extracted_data.append(data)

    df = pd.DataFrame(extracted_data)
    save_dataframe_csv(df, output_path, name)
    return df

def download_file(url:str, path:str):
    '''
    Download a file using a URL and write in a local file
    '''
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        with open(path, 'wb') as file:
            file.write(response.content)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {url, e}")

def parallel_dl(urls, paths, max_workers=8):

    """
    Execute concurrent threads to scrape multiple webpages
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit scraping tasks for each URL and add tqdm progress bar
        futures = [
            executor.submit(
                download_file,
                url,
                path,
            )
            for url, path in zip(urls, paths)
        ]
        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(urls),
            desc="Scraping Progress",
        ):
            try:
                data = future.result()
            except Exception as e:
                print(f"Error downloading : {e}")