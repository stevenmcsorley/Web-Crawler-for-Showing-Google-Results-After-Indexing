import sys
import time
import requests
import re
import json
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from urllib.parse import urljoin


def crawl(base_url, robots_url, data, url_queue, visited_urls, rp, url):
    # Initialize the robot parser
    rp.set_url(robots_url)
    rp.read()

    # Check the value of the crawl-delay directive for your crawler
    crawl_delay = rp.crawl_delay("*")

    # Set a default crawl delay if it is not a number
    crawl_delay = crawl_delay if isinstance(crawl_delay, (int, float)) else 5

    try:
        # Check if the spider is allowed to crawl this url
        if not rp.can_fetch("*", url):
            return data

        # Set the user agent string
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        # Send an HTTP GET request to the given url and return the response
        response = requests.get(url, headers=headers)

        # Wait for the specified time before making the next request
        time.sleep(crawl_delay)

        # read the response
        print(response.status_code)

        # Stop the crawl if the request was rate limited
        if response.status_code == 429:
            print("429 - Too many requests, stopping crawl")
            sys.exit()  # Stop the script

        # Parse the HTML of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the data you want to store
        # check for errors - 'NoneType' object has no attribute 'string'
        title = soup.title
        if title:
            title = title.string
            # Stop the crawl if the title is "Too many requests"
            if title == "Too many requests":
                print("Too many requests, stopping crawl")
                sys.exit()  # Stop the script
        else:
            title = ''

        description = soup.find('meta', attrs={'name': 'description'})
        if description:
            description = description['content']
        else:
            description = ''

        keywords = soup.find('meta', attrs={'name': 'keywords'})
        if keywords:
            keywords = keywords['content']
        else:
            keywords = ''

        # Store the data in the dictionary
        data[url] = {
            'title': title,
            'description': description,
            'keywords': keywords
        }

        # Find all the links on the page
        links = soup.find_all('a')

        # Follow each link
        for link in links:
            href = link.get('href')
            full_url = urljoin(base_url, href)
            base_url_parsed = urlparse(base_url)
            full_url_parsed = urlparse(full_url)
            if full_url_parsed.netloc == base_url_parsed.netloc:
                print(f'Following link: {full_url}')
                if full_url not in visited_urls:
                    url_queue.append(full_url)
                    visited_urls.add(full_url)
            else:
                print(f'Skipping link: {full_url}')

    except Exception as e:
        print(f'An error occurred while crawling {url}: {e}')

    return data


def main():
    # Set the base url and the robots.txt url
    base_url = 'https://kynetik.a2hosted.com'
    robots_url = base_url + '/robots.txt'

    # Initialize the robot parser
    rp = RobotFileParser()

    data = {}
    url_queue = [base_url]
    visited_urls = set()

    while url_queue:
        url = url_queue.pop(0)
        visited_urls.add(url)
        data = crawl(base_url, robots_url, data,
                     url_queue, visited_urls, rp, url)

        # Write the dictionary to a JSON file
        with open('data.json', 'w') as f:
            json.dump(data, f)


if __name__ == '__main__':
    main()
