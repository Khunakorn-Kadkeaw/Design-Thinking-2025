import streamlit as st
import pandas as pd

st.set_page_config(page_title="GPU Price Dashboard", layout="wide")
st.title("📊 GPU Price Dashboard (RTX / RX)")

# ===== อัปโหลดไฟล์ =====
uploaded_file = st.file_uploader("เลือกไฟล์ CSV", type=["csv"])

# ===== โหลดข้อมูล =====
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

if uploaded_file is not None:
    df = load_data(uploaded_file)

    # ===== ทำความสะอาดราคา =====
    df['Price'] = df['Price'].astype(str)
    df['Price'] = df['Price'].str.replace(',', '')
    df['Price'] = df['Price'].astype(int)

    # ===== ดึงรุ่น GPU =====
    df['GPU_Model'] = df['Product'].str.extract(
        r'((RTX|RX)\s?\d{3,4})'
    )[0]

    # ===== Sidebar Filter =====
    st.sidebar.header("Filter")

    series_option = st.sidebar.selectbox(
        "เลือก Series",
        options=["All", "RTX", "RX"]
    )

    if series_option != "All":
        df = df[df['Series'] == series_option]

    # ===== แสดงข้อมูล =====
    st.subheader("📋 ตารางข้อมูล")
    st.dataframe(df)

    # ===== สถิติ =====
    st.subheader("📈 สถิติราคา")

    col1, col2, col3 = st.columns(3)
    col1.metric("จำนวนสินค้า", len(df))
    col2.metric("ราคาเฉลี่ย", f"{df['Price'].mean():,.0f} บาท")
    col3.metric("ราคาสูงสุด", f"{df['Price'].max():,.0f} บาท")

    # ===== กราฟ =====
    st.subheader("📊 ราคาเฉลี่ยแยกตามรุ่น")
    avg_price = df.groupby("GPU_Model")['Price'].mean().sort_values()
    st.bar_chart(avg_price)

else:
    st.info("กรุณาเลือกไฟล์ก่อน")
