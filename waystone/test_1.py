import pandas as pd
import numpy as np
import streamlit as st
n_preview = 15
client_df = None
# Upload area for Client Data
st.write("""Kindly provide the client data in an XLSX file. """)
client_data_file_1= st.file_uploader(":blue[Upload Client Data]", type=['xlsx'], key="client_data1")
client_data_file_2 = st.file_uploader(":blue[Upload Client Data]", type=['xlsx'], key="client_data2")

if client_data_file_1 and client_data_file_2 is not None:
    client_df = pd.read_excel(client_data_file_1)
    client_df_2 = pd.read_excel(client_data_file_2)
    

    st.session_state['client_df'] = client_df
    st.write(f"Preview of Client Data ({n_preview} rows only):")
    st.dataframe(client_df.head(n_preview))
    st.caption(f":green[{len(client_df)}] data rows and :green[{len(client_df.columns)}] columns were loaded.")
    cusip_column = st.selectbox('Select the cusip column :', client_df.columns, key='cusip_col1')
    # Dropdown for selecting the Quantity column
    ticker_column = st.selectbox('Select the ticker column :', client_df.columns, key='ticker_col1')
    st.caption(
        f"""Now we have :green[{len(client_df)}] data rows  in those we have :green[{client_df[cusip_column].isnull().sum()}] missing cusips""")
if st.button('Find Cusips'):
    if client_data_file is not None:
        start_time = time.time()

        mapped_df = parallel_fetch_cusips(client_df, ticker_col=ticker_column, cusip_col=cusip_column)
        end_time = time.time()
        print(end_time - start_time)
        st.dataframe(client_df)
        st.caption(f"Now  we have :green[{client_df[cusip_column].isnull().sum()}] missing cusips")


        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            processed_data = output.getvalue()
            return processed_data


        def main():
            excel_data = to_excel(client_df)
            # Create a download button
            st.download_button(
                label="Download Excel file",
                data=excel_data,
                file_name=f'{client_data_file.name.split(".")[0]}_cleaned.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )


        if __name__ == "__main__":
            main()