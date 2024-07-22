from io import BytesIO

import pandas as pd
import numpy as np
import streamlit as st
n_preview = 15
client_df = None
# Upload area for Client Data
st.subheader("Combined multiple sheets into one sheet ")
st.write("""Kindly provide the client data in an XLSX file. """)
client_data_file= st.file_uploader(":blue[Upload Client Data]", type=['xlsx'], key="client_data_combined")


# Path to the Excel file
# excel_file_path = r"C:\Users\mm3816\Downloads\Client raw files (1)\Octsgon\Portfolio 3.31.24 (2).xlsx"
if client_data_file is not None:

    xls = pd.ExcelFile(client_data_file)

    combined_df = pd.DataFrame()

    # Loop through each sheet name
    for sheet_name in xls.sheet_names:

        df = pd.read_excel(xls, sheet_name=sheet_name)

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



        # Function to filter last 20 rows based on NaN percentage
        last_20_rows = df.tail(20)

        # Count None values in each of the last 10 rows
        none_counts = last_20_rows.isna().sum(axis=1)

        # Calculate the threshold for None values
        none_threshold = 0.6 * len(df.columns)

        # Filter rows where None values exceed the threshold
        filtered_rows = last_20_rows[none_counts >= none_threshold]

        # Drop the identified rows from the original DataFrame
        df.drop(filtered_rows.index, inplace=True)

        #
        df = df.reset_index(drop=True)
        combined_df = combined_df.reset_index(drop=True)
        print(df)
        combined_df = pd.concat([combined_df, df], ignore_index=True, sort=False)
        print(combined_df.index.is_unique)

    # # Save the combined DataFrame to a new Excel file
    # combined_df.to_excel(r'C:\Users\mm3816\Desktop\ravi_files\combined_sheets.xlsx', index=False)

    # print("All sheets have been combined into 'combined_sheets_aligned.xlsx'.")
    # print(combined_df.columns)
    print(combined_df)
    st.dataframe(combined_df)
    if st.button('combine all sheets into one'):
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