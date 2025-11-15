import time

from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
}

my_email=os.getenv("MY_EMAIL")
my_password=os.getenv("MY_PASSWORD")

url="https://www.amazon.com.tr/dp/B08Z4HCGDH"
buy_price=100

while True:

    response=requests.get(url,headers=header)
    soup=BeautifulSoup(response.text,"html.parser")


    title=soup.find(class_="a-size-large product-title-word-break",id="productTitle").getText()

    price=soup.find(class_="a-offscreen").getText()
    price_without=float(price.split("TL")[0].replace(".","").replace(",","."))

    if price_without>100:
        message=f"{title} is on sale for {price}"

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            result = connection.login(my_email,my_password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
            )
    time.sleep(300)