import streamlit as st
import pandas as pd

# ===============================
# 🔷 ตั้งค่าหน้าเว็บ
# ===============================
st.set_page_config(page_title="GPU Price Dashboard", layout="wide")
st.title("📊 GPU Price Dashboard (RTX / RX)")


# ===============================
# 🔷 โหลดข้อมูล (ใช้ cache เพื่อให้แอปเร็วขึ้น)
# ===============================
@st.cache_data  # เก็บข้อมูลไว้ใน memory ป้องกันโหลดไฟล์ซ้ำ
def load_data():
    df = pd.read_csv("cleaned_gpu.csv")  # อ่านไฟล์ CSV
    return df

df = load_data()  # เรียกใช้ฟังก์ชันโหลดข้อมูล


# ===============================
# 🔷 ทำความสะอาดคอลัมน์ราคา
# ===============================
# แปลงราคาเป็น string ก่อน
df['Price'] = df['Price'].astype(str)

# ลบ comma เช่น 12,900 → 12900
df['Price'] = df['Price'].str.replace(',', '')

# แปลงกลับเป็นตัวเลข (int) เพื่อใช้คำนวณได้
df['Price'] = df['Price'].astype(int)


# ===============================
# 🔷 ดึงชื่อรุ่น GPU จาก Product ด้วย Regex
# ===============================
# ตัวอย่าง: "ASUS RTX 4060 8GB GDDR6" → "RTX 4060"
df['GPU_Model'] = df['Product'].str.extract(
    r'((RTX|RX)\s?\d{3,4})'  # หา RTX หรือ RX ตามด้วยเลข 3-4 หลัก
)[0]


# ===============================
# 🔍 Search Box เลือกรุ่น GPU
# ===============================
# เอารุ่นทั้งหมดที่ไม่ซ้ำ และเรียงลำดับ
model_list = sorted(df["GPU_Model"].dropna().unique())

# สร้าง dropdown ให้เลือก
selected_model = st.selectbox(
    "เลือกรุ่น GPU",
    ["ทั้งหมด"] + model_list
)

# ถ้าไม่ได้เลือก "ทั้งหมด" ให้กรองข้อมูลเฉพาะรุ่นนั้น
if selected_model != "ทั้งหมด":
    df = df[df["GPU_Model"] == selected_model]


# ===============================
# 🎚 เลือกช่วงราคา (Slider)
# ===============================
if len(df) > 0:

    # หาราคาต่ำสุด และ สูงสุด
    min_price = int(df["Price"].min())
    max_price = int(df["Price"].max())

    # ถ้ามีมากกว่าราคาเดียว ถึงจะสร้าง slider ได้
    if min_price != max_price:

        # สร้าง slider ให้เลือกช่วงราคา
        price_range = st.slider(
            "เลือกช่วงราคา",
            min_price,
            max_price,
            (min_price, max_price)
        )

        # กรองข้อมูลตามช่วงราคาที่เลือก
        df = df[
            (df["Price"] >= price_range[0]) &
            (df["Price"] <= price_range[1])
        ]

    else:
        st.warning("ข้อมูลมีราคาเดียว ไม่สามารถสร้างช่วงราคาได้")

else:
    # ถ้าไม่มีข้อมูลตรงเงื่อนไข
    st.warning("ไม่พบข้อมูลตามเงื่อนไขที่เลือก")
    st.stop()


# ===============================
# 📊 KPI สรุปภาพรวม
# ===============================
st.subheader("📈 สถิติภาพรวม")

# แบ่งหน้าจอเป็น 4 คอลัมน์
col1, col2, col3, col4 = st.columns(4)

# แสดงค่าทางสถิติ
col1.metric("จำนวนสินค้า", len(df))
col2.metric("ราคาเฉลี่ย", f"{df['Price'].mean():,.0f} บาท")
col3.metric("ราคาสูงสุด", f"{df['Price'].max():,.0f} บาท")
col4.metric("ราคาต่ำสุด", f"{df['Price'].min():,.0f} บาท")


# ===============================
# 📊 เปรียบเทียบ RTX vs RX
# ===============================
st.subheader("📊 เปรียบเทียบ RTX vs RX ในช่วงราคานี้")

# จัดกลุ่มตาม Series แล้วคำนวณราคาเฉลี่ย
series_avg = df.groupby("Series")["Price"].mean()

# แสดงกราฟแท่ง
st.bar_chart(series_avg)


# ===============================
# 📌 แสดงรุ่นที่อยู่ในช่วงราคานี้
# ===============================
st.subheader("📌 รุ่นที่อยู่ในช่วงราคานี้")

# แบ่งหน้าจอเป็น 2 ฝั่ง (RTX / RX)
col1, col2 = st.columns(2)

# -------- ฝั่ง RTX --------
with col1:
    st.write("### RTX")

    # เลือกเฉพาะ Series = RTX และแสดงคอลัมน์ที่ต้องการ
    rtx_models = df[df["Series"] == "RTX"][
        ["Product", "GPU_Model", "VRAM", "Price"]
    ]

    # แสดงตาราง เรียงตามราคาจากน้อยไปมาก
    st.dataframe(
        rtx_models.sort_values("Price"),
        use_container_width=True,
        hide_index=True
    )


# -------- ฝั่ง RX --------
with col2:
    st.write("### RX")

    # เลือกเฉพาะ Series = RX
    rx_models = df[df["Series"] == "RX"][
        ["Product", "GPU_Model", "VRAM", "Price"]
    ]

    # แสดงตาราง
    st.dataframe(
        rx_models.sort_values("Price"),
        use_container_width=True,
        hide_index=True
    )
