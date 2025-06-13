
import streamlit as st
import pandas as pd

# ===== СТИЛЬ CSS =====
st.markdown("""
    <style>
    body {
        background-color: #014421;
        color: #fff;
    }
    .reportview-container {
        background: #014421;
        color: #fff;
    }
    .block-container {
        background-color: #014421;
        color: #fff;
    }
    th, td {
        color: #ffeb3b !important;
    }
    .stDataFrame thead tr th {
        color: #ffeb3b !important;
        background-color: #014421 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 Поиск по исполнительным производствам")

uploaded_file = st.file_uploader("📎 Загрузите файл .ods", type=["ods"])

if uploaded_file:
    try:
        # Чтение с правильной строки заголовков
        df = pd.read_excel(uploaded_file, engine='odf', header=6)
        df.columns = df.columns.astype(str).str.strip()  # Удалим пробелы

        # Сброс индексов и очистка
        df = df.reset_index(drop=True)
        df = df.applymap(lambda x: str(x).strip() if pd.notnull(x) else x)

        # Интерфейс поиска
        search_fullname = st.text_input("🔤 Введите ФИО (Должник) полностью или частично:")
        search_dob = st.text_input("📅 Введите дату рождения (например, 1987-05-09):")

        results = df

        if search_fullname and "Должник" in df.columns:
            results = results[results["Должник"].str.contains(search_fullname, case=False, na=False)]

        if search_dob and "Д.р. должника" in df.columns:
            results = results[results["Д.р. должника"].str.contains(search_dob, na=False)]

        if not results.empty:
            st.success(f"🔍 Найдено совпадений: {len(results)}")
            for idx, row in results.iterrows():
                st.markdown("---")
                st.markdown(f"<h4 style='color:#ffeb3b;'>👤 Должник: {row.get('Должник', '—')}</h4>", unsafe_allow_html=True)
                st.write(f"🏠 Адрес: {row.get('Адрес должника', '—')}")
                st.write(f"🎂 Дата рождения: {row.get('Д.р. должника', '—')}")
                st.write(f"💰 Сумма долга: {row.get('Сумма долга', '—')}")
                st.write(f"📉 Остаток долга: {row.get('Остаток долга', '—')}")
                st.write(f"⚖️ Сумма исп. сбора: {row.get('Сумма исп. сбора', '—')}")
                st.write(f"🧾 Остаток по исп. сбору: {row.get('Остаток по исп. сбору', '—')}")
                st.write(f"🏢 Взыскатель: {row.get('Взыскатель', '—')}")
                st.write(f"📄 Сущность: {row.get('Сущность', '—')}")
        else:
            st.warning("🚫 Совпадений не найдено или нет данных.")
    except Exception as e:
        st.error(f"❌ Ошибка при обработке файла: {e}")
else:
    st.info("👈 Загрузите .ods файл для начала работы.")
