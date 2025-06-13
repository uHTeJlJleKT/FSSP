
import streamlit as st
import pandas as pd

st.title("Поиск по исполнительным производствам")

uploaded_file = st.file_uploader("Загрузите файл .ods", type=["ods"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine='odf', header=1)
    df.columns = df.iloc[0].str.strip()
    df = df[1:]
    df.columns = df.columns.str.strip()
    df = df.rename(columns={
        "Должник": "ФИО",
        "Сумма долга": "СуммаДолга",
        "Остаток долга": "ОстатокДолга",
        "Сумма исп. сбора": "ИспСбор",
        "Остаток по исп. сбору": "ОстатокИспСбора",
        "Взыскатель": "Взыскатель"
    })
    df = df.reset_index(drop=True)
    df = df[1:]  # Удалим строку с заголовками из данных

    # Очистим и переименуем важные поля для удобства
    df = df.rename(columns={
        "Должник": "ФИО",
        "Сумма долга": "СуммаДолга",
        "Остаток долга": "ОстатокДолга",
        "Сумма исп. сбора": "ИспСбор",
        "Остаток по исп. сбору": "ОстатокИспСбора",
        "Взыскатель": "Взыскатель"
    })

    # Ввод данных для поиска
    search_fullname = st.text_input("ФИО полностью или частично:")

    # Фильтрация
    if search_fullname:
        results = df[df['ФИО'].str.contains(search_fullname, case=False, na=False)]
    else:
        results = df

    # Отображение результатов
    if not results.empty:
        for idx, row in results.iterrows():
            st.markdown(f"### 🔍 Должник: {row.get('ФИО', 'Не указано')}")
            st.write(f"**Сумма долга:** {row.get('СуммаДолга', '-')}")
            st.write(f"**Остаток долга:** {row.get('ОстатокДолгa', '-')}")
            st.write(f"**Сумма исп. сбора:** {row.get('ИспСбор', '-')}")
            st.write(f"**Остаток по исп. сбору:** {row.get('ОстатокИспСбора', '-')}")
            st.write(f"**Взыскатель:** {row['Взыскатель']}")
            st.markdown("---")
    else:
        st.info("Ничего не найдено.")
