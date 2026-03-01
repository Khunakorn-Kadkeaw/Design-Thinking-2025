import streamlit as st
import pandas as pd

st.set_page_config(page_title="GPU Price Dashboard", layout="wide")
st.title("📊 GPU Price Dashboard (RTX / RX)")

# ===== โหลดข้อมูลหลังบ้าน =====
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_gpu.csv")
    return df

df = load_data()

# ===== ทำความสะอาดราคา =====
df['Price'] = df['Price'].astype(str)
df['Price'] = df['Price'].str.replace(',', '')
df['Price'] = df['Price'].astype(int)

# ===== ดึงรุ่น GPU =====
df['GPU_Model'] = df['Product'].str.extract(
    r'((RTX|RX)\s?\d{3,4})'
)[0]

# ===============================
# 🔍 Search Box
# ===============================
model_list = sorted(df["GPU_Model"].dropna().unique())

selected_model = st.selectbox(
    "เลือกรุ่น GPU",
    ["ทั้งหมด"] + model_list
)

if selected_model != "ทั้งหมด":
    df = df[df["GPU_Model"] == selected_model]

# ===============================
# 🎚 เลือกช่วงราคา
# ===============================
if len(df) > 0:

    min_price = int(df["Price"].min())
    max_price = int(df["Price"].max())

    if min_price != max_price:

        price_range = st.slider(
            "เลือกช่วงราคา",
            min_price,
            max_price,
            (min_price, max_price)
        )

        df = df[
            (df["Price"] >= price_range[0]) &
            (df["Price"] <= price_range[1])
        ]

    else:
        st.warning("ข้อมูลมีราคาเดียว ไม่สามารถสร้างช่วงราคาได้")

else:
    st.warning("ไม่พบข้อมูลตามเงื่อนไขที่เลือก")
    st.stop()

# ===============================
# 📊 KPI
# ===============================
st.subheader("📈 สถิติภาพรวม")

col1, col2, col3, col4 = st.columns(4)

col1.metric("จำนวนสินค้า", len(df))
col2.metric("ราคาเฉลี่ย", f"{df['Price'].mean():,.0f} บาท")
col3.metric("ราคาสูงสุด", f"{df['Price'].max():,.0f} บาท")
col4.metric("ราคาต่ำสุด", f"{df['Price'].min():,.0f} บาท")

# ===============================
# 📊 เปรียบเทียบ RTX vs RX
# ===============================
st.subheader("📊 เปรียบเทียบ RTX vs RX ในช่วงราคานี้")

series_avg = df.groupby("Series")["Price"].mean()
st.bar_chart(series_avg)

# ===============================
# 📌 รุ่นที่อยู่ในช่วงราคานี้
# ===============================
st.subheader("📌 รุ่นที่อยู่ในช่วงราคานี้")

col1, col2 = st.columns(2)

with col1:
    st.write("### RTX")
    rtx_models = df[df["Series"] == "RTX"][["GPU_Model", "Price"]]
    st.dataframe(rtx_models.sort_values("Price"))

with col2:
    st.write("### RX")
    rx_models = df[df["Series"] == "RX"][["GPU_Model", "Price"]]
    st.dataframe(rx_models.sort_values("Price"))

# ===============================
# 📋 ตารางข้อมูลทั้งหมด
# ===============================
st.subheader("📋 ตารางข้อมูล")
st.dataframe(df)
