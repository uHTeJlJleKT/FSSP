import streamlit as st
import pandas as pd

def compare_tables(table1, table2, key_column):
    table1[key_column] = table1[key_column].astype(str).str.strip()
    table2[key_column] = table2[key_column].astype(str).str.strip()
    result = table1.copy()
    result['Совпадение в таблице 2'] = result[key_column].isin(table2[key_column])
    for column in table1.columns:
        if column == key_column:
            continue
        presence_column = f'{column} заполнено в таблице 2'
        result[presence_column] = result[key_column].map(
            lambda key: pd.notna(
                table2.loc[table2[key_column] == key, column].values[0]
            ) if key in table2[key_column].values and column in table2.columns else False
        )
    return result

def main():
    st.title("🔍 Сравнение таблиц по смыслу заполненности")
    uploaded_file1 = st.file_uploader("Загрузите первую таблицу (шаблон)", type=["csv", "xlsx"])
    uploaded_file2 = st.file_uploader("Загрузите вторую таблицу (для сравнения)", type=["csv", "xlsx"])
    if uploaded_file1 and uploaded_file2:
        filetype1 = uploaded_file1.name.split(".")[-1]
        filetype2 = uploaded_file2.name.split(".")[-1]
        df1 = pd.read_excel(uploaded_file1) if "xls" in filetype1 else pd.read_csv(uploaded_file1)
        df2 = pd.read_excel(uploaded_file2) if "xls" in filetype2 else pd.read_csv(uploaded_file2)
        st.success("✅ Таблицы загружены")
        st.write("Выберите столбец для поиска совпадений:")
        common_columns = list(set(df1.columns) & set(df2.columns))
        if not common_columns:
            st.error("Нет общих столбцов для сравнения.")
            return
        key_column = st.selectbox("🔑 Ключевой столбец:", common_columns)
        if st.button("Сравнить"):
            result_df = compare_tables(df1, df2, key_column)
            st.write("📋 Результаты сравнения:")
            st.dataframe(result_df)
            csv = result_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 Скачать результат в CSV", csv, "comparison_result.csv", "text/csv")

main()