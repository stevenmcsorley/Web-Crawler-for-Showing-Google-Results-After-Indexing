# Web Crawler for Showing Google Results After Indexing

This script is a web crawler that retrieves the title, description, and keywords of a given website and stores them in a dictionary. It also follows links on the page and adds them to a queue to be crawled. The data is then written to a JSON file, which can be used to simulate what the Google search results for the website would look like after the Google bot has indexed it.

## Description of what the code does

The web crawler performs the following actions:

1. Sends an HTTP GET request to the specified base URL and retrieves the HTML of the page.
2. Parses the HTML using the BeautifulSoup library.
3. Extracts the title, description, and keywords from the page's metadata.
4. Stores the extracted data in a dictionary.
5. Finds all the links on the page and adds them to a queue to be crawled.
6. Crawls each link in the queue, repeating the process until there are no more links to follow.
7. Writes the dictionary to a JSON file.

This allows the user to see what the Google search results for the website would look like after the Google bot has indexed it. The crawler respects the rules specified in the `robots.txt` file of the website and is limited to crawling the same domain as the base URL to avoid going too deep into other websites.


## Usage

To use the crawler, run the `main()` function and specify the base URL of the website you want to crawl. The `data.json` file will be created with the crawled data.

## Requirements

- Python 3
- requests library
- BeautifulSoup library
- robotparser library

## Notes

- The crawler respects the rules specified in the `robots.txt` file of the website.
- The crawl is limited to the same domain as the base URL to avoid going too deep into other websites.

## Future Improvements

- Add command line arguments to specify the base URL and output file name.
- Implement threading or asynchronous IO to speed up the crawl.
- Add more data to the dictionary, such as the date the page was last modified and the size of the page.
- Persist the data to a database instead of a JSON file.
