import pandas as pd
import numpy as np
import streamlit as st
n_preview=15
client_df = None
    # Upload area for Client Data
client_data_file = st.file_uploader(":blue[Upload Client Data]", type=['xlsx'], key="client_data")
if client_data_file is not None:
    client_df = pd.read_excel(client_data_file)
    st.session_state['client_df'] = client_df
    st.write(f"Preview of Client Data ({n_preview} rows only):")
    st.dataframe(client_df.head(n_preview))
    st.caption(f":green[{len(client_df)}] data rows and :green[{len(client_df.columns)}] columns were loaded")

    # Dropdown for selecting the CUSIP column
    cusip_column = st.selectbox('Select the Identifier column:*', client_df.columns, key='cusip_col')
    # Dropdown for selecting the Quantity column

    quantity_column = st.selectbox('Select the Quantity column:*', client_df.columns, key='quantity_col', index=1)
    client_df = client_df.rename({cusip_column: "underlying cusip",quantity_column:"quantity"}, axis=1)
    st.dataframe(client_df.head(n_preview))
    # client_df_columns = list(client_df.columns)
    # client_df_columns.append(None)
    # desc_column = st.selectbox('Select the Description column:*', client_df_columns,
    #                            index=client_df_columns.index(None), key='description1')
    # price_column = st.selectbox("Select the Price column:*", client_df_columns, index=client_df_columns.index(None),
    #                             key='price1')
    # market_value_column = st.selectbox("Select the Market column:*", client_df_columns,
    #                                    index=client_df_columns.index(None), key='market_value1')
