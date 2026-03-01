# [ชื่อโครงงาน- Computer Hardware Price Tracker]

แอปพลิเคชัน Streamlit สำหรับติดตามราคาการ์ดจอ (GPU) จากเว็บไซต์ JIB โดยใช้เทคนิค Web Scraping เพื่อเก็บข้อมูลชื่อสินค้า รุ่น (RTX / RX) 
และราคา แล้วนำมาแสดงผลเป็น Dashboard สำหรับวิเคราะห์แนวโน้มราคา
กลุ่มเป้าหมาย:
ผู้ที่ต้องการซื้อการ์ดจอ
เกมเมอร์
นักประกอบคอม
นักวิเคราะห์ข้อมูล

ปัญหาที่ช่วยแก้:
ช่วยติดตามและเปรียบเทียบราคาการ์ดจอได้ง่ายขึ้น โดยไม่ต้องเข้าเว็บทุกวัน

## 🚀 ฟีเจอร์หลัก (Features)
Web Scraping ดึงข้อมูลอัตโนมัติ
ชื่อรุ่น (GPU Model)
ราคา (Price)
Series (RTX / RX)

ระบบ Data Cleaning และจัดรูปแบบข้อมูล
แยก Series ออกเป็น RTX และ RX
แปลงราคาจากข้อความเป็นตัวเลข
จัดโครงสร้าง DataFrame ให้พร้อมใช้งาน

การแสดงผลแบบแยก Series (RTX vs RX)
Dashboard แสดงข้อมูลแบบแบ่งคอลัมน์
ฝั่งซ้ายแสดงรุ่น RTX
ฝั่งขวาแสดงรุ่น RX
เรียงราคาจากน้อยไปมาก

ระบบกรองช่วงราคา (Price Range Filter)
ผู้ใช้สามารถเลือกช่วงราคาที่สนใจได้
ระบบจะแสดงเฉพาะรุ่นที่อยู่ในงบประมาณนั้น
เหมาะสำหรับผู้ที่ต้องการเลือกการ์ดจอตามงบประมาณที่กำหนด

## 👥 สมาชิกและภาระงาน (Team Members & Responsibilities)

ตารางแสดงการแบ่งงานรายสัปดาห์ระหว่างสมาชิกทั้ง 2 คน:

| สัปดาห์ที่ (Week) | [นาย คุณากร กาดแก้ว 67026966] 
| :--- | :--- | :--- |
| **Week 1** | วางแผนโครงงาน | สร้าง code Scrape 
| **Week 2** | ปรับแก้ไข code Scraping | test ระบบ Scraping
| **Week 3** | ออกแบบหน้าเว็ปไซต์ streamlit
| **Week 4** | สร้างเว็ปไซต์ streamlit | test ระบบ streamlit และ ทำสรุป

---

## 🛠️ เทคโนโลยีที่ใช้ (Tech Stack)
Language: Python
Framework: Streamlit
Libraries:
Pandas
BeautifulSoup
Requests
Plotly / Matplotlib

## 📦 การติดตั้งและการใช้งาน (Setup & Installation)
1. ทำการโหลด python จาก 'https://www.python.org/downloads/'
2. ทำการติดตั้ง VScode เพื่อใช้ในการการสกัดข้อมูล จาก 'https://code.visualstudio.com/download'
3. ทำการสกัดข้อมูลที่ต้องใช้ ใน VScode ด้วยภาษา python 'https://github.com/Makin-Thaijaroen/Design-Thinking-2025/blob/main/Design.py'
4. ทำการเชื่อม Steamlit กับ github เพื่อที่จะได้สร้างหน้าเว็ป 'https://share.streamlit.io/?utm_source=streamlit&utm_medium=referral&utm_campaign=main&utm_content=-ss-streamlit-io-topright'
5. นำไฟล์ csv ที่ได้จากการ scraping มาอัปโหลดใน github เพื่อที่จะได้นำไฟล์ csv มาใช้ในการสร้างเว็ป

## 🧾 เอกสารอ้างอิงที่ใช่ในการทำงาน
- เว็ปที่ใช้ในการ scraping ข้อมูล 'https://www.jib.co.th/web/?srsltid=AfmBOoo3Z6llj-mSbuWRLD33A3qEVMe7GF6Isn6HNUshxsZdqygkTHc2'
- Source code ที่ใช่ในการ scraping ข้อมูล และการสร้างเว็ป แนวทางมาจาก ChatGPT

💡 สะท้อนคิด
โปรเจคนี้เป็นการพัฒนา Web Dashboard ด้วย Streamlit เพื่อวิเคราะห์และแสดงผลข้อมูลการ์ดจอ (GPU) โดยข้อมูลไม่ได้มีอยู่แล้ว แต่ได้มาจากการทำ Web Scraping จากเว็บไซต์ขายสินค้า จากนั้นนำมาทำความสะอาด วิเคราะห์ และสร้าง Dashboard 
และการใช้ GitHub เพื่อทำงาน รวมถึงการวางแผนอย่างเป็นระบบ เข้าใจโครงสร้าง HTML ของเว็บไซต์ เรียนรู้การดึงข้อมูล เช่น ชื่อสินค้า ราคา และรายละเอียดสเปก เข้าใจว่าข้อมูลจากเว็บมักไม่สะอาด และต้องจัดการก่อนใช้งาน ฝึกจัดเก็บข้อมูลเป็น CSV เพื่อใช้ต่อในการวิเคราะห์

1. **Clone repository นี้:**
   ```bash
git clone https://github.com/Khunakorn-Kadkeaw/Design-Thinking-2025.git
cd Design-Thinking-2025
