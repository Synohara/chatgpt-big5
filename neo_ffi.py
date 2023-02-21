import requests
from bs4 import BeautifulSoup

response = requests.get("http://www.sinritest.com/bigfive01.html")

with open("index.html") as f:
    lines = f.read()
    
soup = BeautifulSoup(lines, 'html.parser')

q_list = []
a_list = []
for t in soup.find_all(class_="text"):
    if "Q" in t.text:
        # print(t.text)
        q_list.append(t.text)

for t in soup.find_all("input"):
    if t.has_attr("data-com.bitwarden.browser.user-edited"):
        # print(t.get("value"))
        a_list.append(t.get("value"))

for q, a in zip(q_list, a_list):
    print(q)