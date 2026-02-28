from scraper.jib_scraper import scrape_jib
import pandas as pd

url = "https://www.jib.co.th/web/product/product_list/2/51"

data = scrape_jib(url)

df = pd.DataFrame(data)
df.to_csv("data/raw_gpu.csv", index=False)

print("Scraping complete!")
