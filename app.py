import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit.components.v1 import html

# ---------------------- Cấu hình giao diện ----------------------
st.set_page_config(
    page_title="YData Profiling App",
    layout="wide",
    page_icon="📊"
)

st.title("📊 YData Profiling Report")
st.markdown("Tạo báo cáo tự động từ file dữ liệu (.csv hoặc .xlsx)")

# ---------------------- Sidebar ----------------------
st.sidebar.header("⚙️ Cấu hình")

uploaded_file = st.sidebar.file_uploader(
    "Upload .csv hoặc .xlsx (tối đa 10MB)",
    type=["csv", "xlsx"]
)

mode = st.sidebar.radio("Modes of Operation", ["Explorative", "Minimal"])
display_mode = st.sidebar.radio("Display mode", ["Primary", "Dark", "Orange"], index=0)

# ---------------------- Đọc file ----------------------
if uploaded_file is not None:
    file_name = uploaded_file.name

    # Đọc file Excel hoặc CSV
    if file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        excel = pd.ExcelFile(uploaded_file)
        sheet_name = st.sidebar.selectbox("Select sheet", excel.sheet_names)
        df = excel.parse(sheet_name)

    st.write(f"✅ Đã tải dữ liệu: `{file_name}` ({df.shape[0]} dòng × {df.shape[1]} cột)")

    # ---------------------- Sinh báo cáo ----------------------
    minimal = mode == "Minimal"

    with st.spinner("🔍 Đang tạo báo cáo... vui lòng chờ..."):
        profile = ProfileReport(
            df,
            title="YData Profiling Report",
            explorative=not minimal,
            minimal=minimal
        )
        report_html = profile.to_html()

    # ---------------------- Hiển thị ----------------------
    st.success("✅ Báo cáo đã sẵn sàng!")

    # CSS ép màu sáng, giúp hiển thị rõ hơn
    st.markdown(
        """
        <style>
            iframe {
                background-color: white !important;
                color: black !important;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
            body {
                background-color: #f9f9f9 !important;
                color: black !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    html(report_html, height=1000, scrolling=True)

else:
    st.info("⬆️ Hãy tải lên file dữ liệu để bắt đầu.")