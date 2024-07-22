# combined all sheets into one
from io import BytesIO

import pandas as pd
import streamlit as st
import numpy as np

import xlrd
n_preview=15
client_df = None
    # Upload area for Client Data
client_data_file_1 = st.file_uploader(":blue[Upload Client Data first file]", type=['xlsx'], key="client_data1")

client_data_file_2 = st.file_uploader(":blue[Upload Client Data second file]", type=['xlsx'], key="client_data2")

if client_data_file_1 and client_data_file_2 is not None:
    client_df_1= pd.read_excel(client_data_file_1)
    st.session_state['client_df_1'] = client_df_1
    st.write(f"Preview of Client Data ({n_preview} rows only):")
    st.dataframe(client_df_1.head(n_preview))
    st.caption(f":green[{len(client_df_1)}] data rows and :green[{len(client_df_1.columns)}] columns were loaded")
    client_df_2 = pd.read_excel(client_data_file_2)
    st.session_state['client_df_2'] = client_df_2
    st.write(f"Preview of Client Data ({n_preview} rows only):")
    st.dataframe(client_df_2.head(n_preview))
    st.caption(f":green[{len(client_df_2)}] data rows and :green[{len(client_df_2.columns)}] columns were loaded")

    # list_of_path = [r"C:\Users\mm3816\Downloads\rebluespruceq213fdata\Portfolio Report_P3-CMDY LLC_03292024.xlsx",
    #                 r"C:\Users\mm3816\Downloads\rebluespruceq213fdata\Portfolio Report_Sachem_03292024.xlsx"]
    list_of_path  = []
    # print("client_data_file_1",client_data_file_1)
    list_of_path.append(client_data_file_1)
    list_of_path.append(client_data_file_2)
    print(list_of_path)
    combined_df = pd.DataFrame()
    for i in list_of_path:
        # xls = pd.ExcelFile(i)

        df = pd.read_excel(i)

        unnamed_columns = df.columns[df.columns.str.startswith('Unnamed:') & ~df.columns.isna()]

        percentage_unnamed = len(unnamed_columns) / len(df.columns)

        # Check if more than 70% of columns start with 'Unnamed:'
        if percentage_unnamed > 0.7:
            # Replace column names with the first row values
            df.columns = df.iloc[0]  # .fillna(df.columns)
            # Drop the first row
            df = df.drop(df.index[0])

        nan_count = df.columns.isnull().sum()
        total_columns = len(df.columns)
        nan_proportion = nan_count / total_columns

        # Check if more than half of the column names are NaN
        if nan_proportion > 0.7:
            while any(pd.isna(df.columns)):
                # Replace column names with the first row values
                df.columns = df.iloc[0]  # .fillna(df.columns)
                # Drop the first row
                df = df.drop(df.index[0])

        # Reset the index if needed
        df.reset_index(drop=True, inplace=True)
        # Extract the last 10 rows
        last_20_rows = df.tail(20)

        # Count None values in each of the last 10 rows
        none_counts = last_20_rows.isna().sum(axis=1)
        # print("none_counts",none_counts)
        # Calculate the threshold for None values
        none_threshold = 0.6 * len(df.columns)
        # print("none_threshold",none_threshold)
        # Filter rows where None values exceed the threshold
        filtered_rows = last_20_rows[none_counts >= none_threshold]
        # print("filtered_rows\n",filtered_rows)
        # Drop the identified rows from the original DataFrame
        df.drop(filtered_rows.index, inplace=True)

        df = df.reset_index(drop=True)
        combined_df = combined_df.reset_index(drop=True)
        combined_df = pd.concat([combined_df, df], ignore_index=True, sort=False)
        print(combined_df.index.is_unique)

    print(combined_df)
    if st.button('merged_the_data'):
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            processed_data = output.getvalue()
            return processed_data


        def main():
            excel_data = to_excel(combined_df)
            # Create a download button
            st.download_button(
                label="Download Excel file",
                data=excel_data,
                file_name=f'cleaned.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )


        if __name__ == "__main__":
            main()
    # st.dataframe(combined_df)
    # st.write(combined_df)