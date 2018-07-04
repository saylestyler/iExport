#!/usr/bin/zsh

import requests
from bs4 import BeautifulSoup

# prints all elements on this url with the tag a href
# # sample output from chase.com
# # <a href='#main'>Skip to main content</a>
# # Close Side Menu
# # </a>
# # <a href='https://www.chase.com'>
# # Home
# # </a>
# # <a href='https://chaseonline.chase.com/'>
# # Sign in
# # </a>
url = "http://www.chase.com/"
r = requests.get(url)
soup = BeautifulSoup(r.content, "lxml")
links = soup.find_all("a")

for link in links:
    print "<a href='%s'>%s</a>" % (link.get("href"), link.text)

g_data = soup.find_all("div", {"class": "info"})
