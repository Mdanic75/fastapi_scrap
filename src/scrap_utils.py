from bs4 import BeautifulSoup
import re
from typing import List


class Scraper:
    def __init__(self, html_as_text: str):
        self.soup = BeautifulSoup(html_as_text, "html.parser")
        self.phone_numbers = self.find_phone_numbers()
        self.links = self.find_all_links()
        self.social_media_links = self.filter_social_media_links()

    def find_phone_numbers(self) -> List[str]:
        phone_regex = re.compile(r'\(?\b[0-9]{3}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}\b')
        phone_numbers = re.findall(phone_regex, self.soup.text)
        return phone_numbers

    def find_all_links(self) -> List[str]:
        links = []
        for a_tag in self.soup.find_all('a', href=True):
            if a_tag["href"].startswith("http") and not a_tag['href'].endswith(('.jpg', '.png', '.jpeg', '.gif')):
                links.append(a_tag["href"])
        return links

    def filter_social_media_links(self) -> List[str]:
        social_media_links = []
        social_media_domains = ["facebook.com", "twitter.com", "linkedin.com", "instagram.com", "youtube.com",
                          "pinterest.com", "tumblr.com"]
        new_links = []
        for i in range(len(self.links)):
            if any(domain in self.links[i] for domain in social_media_domains):
                social_media_links.append(self.links[i])
            else:
                new_links.append(self.links[i])
        self.links = new_links
        return social_media_links
