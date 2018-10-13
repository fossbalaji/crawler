from urllib import request, parse
from bs4 import BeautifulSoup
import logging


class Crawlutils(object):
    """
        author: fossbalaji@gmail.com,
        purpose: to crawl a webpage by given depth
    """
    def canonicalize(self, url):
        parts = list(parse.urlparse(url))
        if parts[2] == '':
            parts[2] = '/'  # Empty path equals root path
        parts[5] = ''  # Erase fragment
        return parse.urlunparse(parts)

    def fetch(self, url):
        logging.info('Fetching %s', url)
        response = request.urlopen(url, timeout=5)
        assert response.status == 200
        data = response.read()
        assert data
        return data

    def same_domain(self, a, b):
        parsed_a = parse.urlparse(a)
        parsed_b = parse.urlparse(b)
        if parsed_a.netloc == parsed_b.netloc:
            return True
        if (parsed_a.netloc == '') ^ (parsed_b.netloc == ''):  # Relative paths
            return True
        return False

    def get_domain(self, a):
        parsed_a = parse.urlparse(a)
        return parsed_a.netloc

    def extract(self, url):
        data = self.fetch(url)
        found_urls = set()
        img_urls = set()
        content = BeautifulSoup(data, "html.parser")

        for link in content.findAll('a'):
            found = self.canonicalize(url=link.get("href"))
            if self.same_domain(url, found):
                found_urls.add(parse.urljoin(url, found))

        for link in content.findAll('img'):
            found = self.canonicalize(url=link.get('src'))
            if "http://" or "https://" in found:
                img_urls.add(parse.urljoin(url,found))

        return url, data, sorted(found_urls), sorted(img_urls)

    def extract_multi(self, to_fetch, seen_urls):
        results = []
        for url in to_fetch:
            if url in seen_urls:
                continue
            seen_urls.add(url)
            try:
                results.append(self.extract(url))
            except Exception as e:
                print(str(e))
                continue
        return results

    def crawl(self, start_url, max_depth):
        seen_urls = set()
        to_fetch = [self.canonicalize(url=start_url)]
        results = []
        for depth in range(max_depth + 1):
            batch = self.extract_multi(to_fetch, seen_urls)
            to_fetch = []
            for url, data, found_urls, img_urls in batch:
                results.append((depth, url, data, found_urls, img_urls))
                to_fetch.extend(found_urls)
        return {"domain": self.get_domain(a=start_url), "results": results}
