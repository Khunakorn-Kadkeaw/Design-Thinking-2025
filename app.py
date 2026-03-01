{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOIbBX1XjDJdP7QiUiMJain",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Khunakorn-Kadkeaw/Design-Thinking-2025/blob/main/app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 14,
      "metadata": {
        "id": "5Y3KsJTricAX",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "07df557e-7d3f-436b-c017-5c447e268054"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "2026-03-01 20:53:49.854 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-01 20:53:49.856 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-01 20:53:49.856 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-01 20:53:49.857 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-01 20:53:49.858 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-01 20:53:49.859 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-01 20:53:49.860 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-01 20:53:49.860 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-01 20:53:49.861 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-01 20:53:49.861 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-01 20:53:49.863 No runtime found, using MemoryCacheStorageManager\n",
            "2026-03-01 20:53:49.864 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-01 20:53:49.865 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2026-03-01 20:53:49.866 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
          ]
        }
      ],
      "source": [
        "import streamlit as st\n",
        "import pandas as pd\n",
        "\n",
        "st.set_page_config(page_title=\"GPU Price Dashboard\", layout=\"wide\")\n",
        "st.title(\"📊 GPU Price Dashboard (RTX / RX)\")\n",
        "\n",
        "# ===== อัปโหลดไฟล์ =====\n",
        "uploaded_file = st.file_uploader(\"เลือกไฟล์ CSV\", type=[\"csv\"])\n",
        "\n",
        "# ===== โหลดข้อมูล =====\n",
        "@st.cache_data\n",
        "def load_data(file):\n",
        "    df = pd.read_csv(file)\n",
        "    return df\n",
        "\n",
        "if uploaded_file is not None:\n",
        "    df = load_data(uploaded_file)\n",
        "\n",
        "    # ===== ทำความสะอาดราคา =====\n",
        "    df['Price'] = df['Price'].astype(str)\n",
        "    df['Price'] = df['Price'].str.replace(',', '')\n",
        "    df['Price'] = df['Price'].astype(int)\n",
        "\n",
        "    # ===== ดึงรุ่น GPU =====\n",
        "    df['GPU_Model'] = df['Product'].str.extract(\n",
        "        r'((RTX|RX)\\s?\\d{3,4})'\n",
        "    )[0]\n",
        "\n",
        "    # ===== Sidebar Filter =====\n",
        "    st.sidebar.header(\"Filter\")\n",
        "\n",
        "    series_option = st.sidebar.selectbox(\n",
        "        \"เลือก Series\",\n",
        "        options=[\"All\", \"RTX\", \"RX\"]\n",
        "    )\n",
        "\n",
        "    if series_option != \"All\":\n",
        "        df = df[df['Series'] == series_option]\n",
        "\n",
        "    # ===== แสดงข้อมูล =====\n",
        "    st.subheader(\"📋 ตารางข้อมูล\")\n",
        "    st.dataframe(df)\n",
        "\n",
        "    # ===== สถิติ =====\n",
        "    st.subheader(\"📈 สถิติราคา\")\n",
        "\n",
        "    col1, col2, col3 = st.columns(3)\n",
        "    col1.metric(\"จำนวนสินค้า\", len(df))\n",
        "    col2.metric(\"ราคาเฉลี่ย\", f\"{df['Price'].mean():,.0f} บาท\")\n",
        "    col3.metric(\"ราคาสูงสุด\", f\"{df['Price'].max():,.0f} บาท\")\n",
        "\n",
        "    # ===== กราฟ =====\n",
        "    st.subheader(\"📊 ราคาเฉลี่ยแยกตามรุ่น\")\n",
        "    avg_price = df.groupby(\"GPU_Model\")['Price'].mean().sort_values()\n",
        "    st.bar_chart(avg_price)\n",
        "\n",
        "else:\n",
        "    st.info(\"กรุณาเลือกไฟล์ก่อน\")"
      ]
    }
  ]
}