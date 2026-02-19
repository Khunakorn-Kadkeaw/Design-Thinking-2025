import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = "https://www.jib.co.th/web/product/product_list/2/51"

headers = {
    "User-Agent": "Mozilla/5.0"
}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

# container สินค้าแต่ละชิ้น
items = soup.find_all("div", class_="col-md-3 col-sm-4 col-xs-6 divboxpro")

data = []

for item in items:

    # ===== ดึงชื่อ =====
    name_tag = item.find("span", class_="promo_name")
    if not name_tag:
        continue
    name = name_tag.text.strip()

    # ===== ดึงราคา =====
    price_tag = item.find("p", class_="price_total")
    if not price_tag:
        continue
    price_text = price_tag.text.strip()

    # ล้างให้เหลือเลข
    price_number = re.sub(r"[^\d]", "", price_text)

    # ===== แยก RTX / RX =====
    name_upper = name.upper()

    if re.search(r"\bRTX\b", name_upper):
        series = "RTX"
    elif re.search(r"\bRX\b", name_upper):
        series = "RX"
    else:
        series = "Other"

    # ===== เก็บข้อมูล =====
    data.append({
        "Product": name,
        "Series": series,
        "Price": price_number
    })

# แปลงเป็น DataFrame
df = pd.DataFrame(data)
print(df)

# บันทึกไฟล์
df.to_csv("gpu_prices.csv", index=False, encoding="utf-8-sig")

print("บันทึกไฟล์ recipes_dataset.csv สำเร็จ")
