import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")

# Set the title of the web app
st.title("Internal - Schematic vs Layout Comparer")
st.divider()

# Upload two Excel files
col1, col2 = st.columns(2)

with col1:
    file1 = st.file_uploader("Upload the SCHEMATIC Excel File", type=["xlsx", "xls"])

with col2:
    file2 = st.file_uploader("Upload the LAYOUT Excel File", type=["xlsx", "xls"])

if file1 and file2:
    # Read the Excel files into DataFrames
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Function to remove leading zeros from strings
    def remove_leading_zeros(val):
        if isinstance(val, str):
            return val.lstrip('0')
        return val

    # Apply the function to each cell in both DataFrames
    df1 = df1.applymap(remove_leading_zeros)
    df2 = df2.applymap(remove_leading_zeros)

    # Convert all text data to lowercase for case-insensitive comparison
    df1 = df1.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    df2 = df2.applymap(lambda x: x.lower() if isinstance(x, str) else x)

    # Split CSV data into rows
    csv_file1 = df1.to_csv(index=False, encoding="utf-8", header=False)
    csv_file2 = df2.to_csv(index=False, encoding="utf-8", header=False)

    # Split CSV data into rows and store them in lists
    rows1 = csv_file1.split("\n")
    rows2 = csv_file2.split("\n")

    # Find rows from the first file that are not in the second file
    unique_rows = [row for row in rows1 if row not in rows2]

    # if unique_rows:
    #     st.write("Rows from the first file that are not in the second file:")
    #     st.text("\n".join(unique_rows))
    # else:
    #     st.write("All rows from the first file are also in the second file.")

    # Find items in the first column of the second file not in the first file
    col1_second_file = df2.iloc[:, 0].tolist()
    col1_first_file = df1.iloc[:, 0].tolist()
    missing_items = [item for item in col1_second_file if item not in col1_first_file]

    # Add empty rows in the first DataFrame at the index locations of missing items
    for item in missing_items:
        index = col1_second_file.index(item)
        empty_row = [None] * df1.shape[1]
        df1 = df1.iloc[:index].append(pd.Series(empty_row, index=df1.columns), ignore_index=True).append(df1.iloc[index:], ignore_index=True)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <style>
            .left-aligned-title {
                text-align: left;
            }
        </style>
    """, unsafe_allow_html=True)

        st.markdown('<h1 class="left-aligned-title">Schematic</h1>', unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <style>
            .right-aligned-title {
                text-align: right;
            }
        </style>
    """, unsafe_allow_html=True)

        st.markdown('<h1 class="right-aligned-title">Layout</h1>', unsafe_allow_html=True)


    df_empty = pd.DataFrame({' ': [" "] * len(df1)})

    result_list = []

    for item in unique_rows:
        split_items = item.split(',')
        result_list.extend(split_items)

    def highlight_diff(row):
        if row['Part Reference'] in result_list:
            return ['background-color: yellow'] * len(row)
        
        elif row['Part Reference'] in [None]:
            return ['background-color: cyan'] * len(row)

        else:
            return [''] * len(row)

    test = pd.concat([df1, df_empty, df2], axis=1, join='inner')
    st.dataframe(test.style.apply(highlight_diff, axis=1), height=600, width=1800)


