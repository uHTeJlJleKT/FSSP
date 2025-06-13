
import streamlit as st
import pandas as pd

st.title("🔍 Поиск по исполнительным производствам")

uploaded_file = st.file_uploader("📎 Загрузите файл .ods", type=["ods"])

if uploaded_file:
    try:
        # Чтение с правильной строки заголовков
        df = pd.read_excel(uploaded_file, engine='odf', header=6)
        df.columns = df.columns.astype(str).str.strip()  # Удалим пробелы

        # Переименование столбцов, если они есть
        column_mapping = {
            "Должник": "ФИО",
            "Сумма долга": "СуммаДолга",
            "Остаток долга": "ОстатокДолга",
            "Сумма исп. сбора": "ИспСбор",
            "Остаток по исп. сбору": "ОстатокИспСбора",
            "Взыскатель": "Взыскатель",
            "Д.р. должника": "ДатаРождения"
        }
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        df = df.reset_index(drop=True)

        df = df.applymap(lambda x: str(x).strip() if pd.notnull(x) else x)

        # Интерфейс поиска
        search_fullname = st.text_input("🔤 Введите ФИО полностью или частично:")
        search_dob = st.text_input("📅 Введите дату рождения (например, 1987-05-09):")

        results = df

        if search_fullname and "ФИО" in df.columns:
            results = results[results["ФИО"].str.contains(search_fullname, case=False, na=False)]

        if search_dob and "ДатаРождения" in df.columns:
            results = results[results["ДатаРождения"].str.contains(search_dob, na=False)]

        if not results.empty:
            st.success(f"🔍 Найдено совпадений: {len(results)}")
            for idx, row in results.iterrows():
                st.markdown("---")
                st.markdown(f"### 👤 Должник: {row.get('ФИО', '—')}")
                st.write(f"**🎂 Дата рождения:** {row.get('ДатаРождения', '—')}")
                st.write(f"**💰 Сумма долга:** {row.get('СуммаДолга', '—')}")
                st.write(f"**📉 Остаток долга:** {row.get('ОстатокДолга', '—')}")
                st.write(f"**⚖️ Сумма исп. сбора:** {row.get('ИспСбор', '—')}")
                st.write(f"**🧾 Остаток по исп. сбору:** {row.get('ОстатокИспСбора', '—')}")
                st.write(f"**🏢 Взыскатель:** {row.get('Взыскатель', '—')}")
        else:
            st.warning("🚫 Совпадений не найдено или нет данных.")
    except Exception as e:
        st.error(f"❌ Ошибка при обработке файла: {e}")
else:
    st.info("👈 Загрузите .ods файл для начала работы.")
