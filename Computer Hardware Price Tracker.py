import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = "https://www.jib.co.th/web/product/product_list/2/51"

#คือการกำหนด HTTP Header
#เพื่อบอกเว็บไซต์ว่า:ฉันคือ Browser  ไม่ใช่ Bot
#User-Agent คือข้อความที่บอกว่า: ใช้ Browser อะไร /ใช้ระบบปฏิบัติการอะไร
#เพื่อให้เว็บคิดว่าเป็น browser ทั่วไป
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

#ส่ง HTTP GET request
#Server ของเว็บรับคำขอ\Server ส่ง HTML กลับมา
#เก็บไว้ในตัวแปร page

#เอา HTML ดิบที่ได้จากเว็บ → แปลงให้กลายเป็นโครงสร้างที่ค้นหา tag ได้
#BeautifulSoup : อ่าน HTML ทั้งหมด แยก tag ออก สร้างโครงสร้างแบบต้นไม้ เก็บไว้ในตัวแปร soup
#page.content ดึง: HTML ทั้งหมดของหน้าเว็บ
#'html.parser' : คือการบอก BeautifulSoup ว่า:ใช้วิธีไหนในการแปล HTML
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

# container สินค้าแต่ละชิ้น
#ค้นหา tag <div> ทุกตัว ที่มี class ตรงตามที่กำหนด แล้วเก็บไว้ในตัวแปร items
#soup.find_all : ค้นหา element ใน HTML tree
#คืนค่ากลับมาเป็น “รายการ (list)” ของ tag ที่ตรงเงื่อนไข
items = soup.find_all("div", class_="col-md-3 col-sm-4 col-xs-6 divboxpro")

#คือการสร้าง list ว่าง  ไว้สำหรับเก็บข้อมูลที่เราจะดึงจากเว็บ
data = []

 # ===== ดึงชื่อจาก ตัวแปร items =====
 #โดยการค้นหา tag <span> ตัวแรกที่มี class ตรงตามที่กำหนดภายในสินค้าแต่ละรายการ แล้วเก็บไว้ในตัวแปร name_tag
 
 #จากนั้นตรวจสอบว่าพบ tag ชื่อสินค้าหรือไม่
 #หากไม่พบจะข้ามรายการนั้นเพื่อป้องกันข้อผิดพลาด 
 #จากนั้นจึงดึงข้อความภายใน tag และลบช่องว่างส่วนเกินออก แล้วเก็บไว้ใน name
for item in items:
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
    #ลบทุกอย่างที่ไม่ใช่ตัวเลขออกจาก price_text
    price_number = re.sub(r"[^\d]", "", price_text)
    
    # แปลงชื่อสินค้าเป็นตัวพิมพ์ใหญ่ แล้วตรวจสอบว่ามีคำว่า RTX หรือ RX
    # เพื่อจัดประเภทการ์ดจอ หากไม่พบจะจัดเป็น Other
    #\b : ขอบเขตของคำ เพื่อให้แน่ใจว่าค้นหาเฉพาะคำว่า RTX หรือ RX
    # ===== แยก RTX / RX =====
    name_upper = name.upper()

    if re.search(r"\bRTX\b", name_upper):
        series = "RTX"
    elif re.search(r"\bRX\b", name_upper):
        series = "RX"
    else:
        series = "Other"

    # เพิ่มข้อมูลสินค้าแต่ละรายการลงใน list data ในรูปแบบ Dictionary
    #ทำให้ข้อมูลถูกจัดเก็บเป็นโครงสร้างแบบตาราง ซึ่งสามารถนำไปสร้างเป็น DataFrame ของ pandas ต่อได้ง่าย
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

# Data Cleaning
#ลบข้อมูลซ้ำ
#เว็บบางทีมีสินค้าเดิมซ้ำ
#ถ้าไม่ลบ → วิเคราะห์ผิด
df = df.drop_duplicates()

#แปลงราคาเป็นตัวเลข
#ตอน scrape ราคายังเป็น string
#ถ้าไม่แปลง → คำนวณค่าเฉลี่ยไม่ได้
df['Price'] = df['Price'].astype(str)
df['Price'] = df['Price'].str.replace(',', '')
df['Price'] = df['Price'].astype(int)

#ตรวจ Missing Value
#เช็คว่ามีข้อมูลหายไหม
#ถ้ามี → ต้องจัดการก่อนวิเคราะห์
df.isnull().sum()

#Feature Engineering
#ดึงเฉพาะชื่อรุ่น 

#เพราะชื่อสินค้าเต็ม ๆ ใช้วิเคราะห์ยาก
#ต้องการ “รุ่นการ์ดจอ” เป็นตัวแปรหลัก
df['GPU_Model'] = df['Product'].str.extract(r'((RTX|RX)\s?\d{3,4})')[0]
# ===== Extract VRAM =====
df["VRAM"] = df["Product"].str.extract(
    r"(\d+\s?GB)",
    expand=False
)

#Export Data ที่ทำความสะอาดแล้ว
import os
os.makedirs("data", exist_ok=True)
df.to_csv("data/cleaned_gpu.csv", index=False)
