# url = f"https://stockanalysis.com/stocks/{ticker}/company/"
        #
        # try:
        #     # Attempt to fetch the page
        #     response = requests.get(url, timeout=10)  # Added timeout for the request
        #     # Check if the request was successful
        #     response.raise_for_status()
        # except requests.RequestException as e:
        #     print(f"Failed to retrieve page: {e}")
        #     return None
        #
        # try:
        #     page = requests.get(url)
        #     tree = html.fromstring(page.content)
        #
        #     # Define the XPath to extract the buyers information
        #     xpath_expression = '//*[@id="main"]/div[2]/div[2]/div[3]/table/tbody/tr[6]/td[2]'
        #     try:
        #         # Use xpath() method to extract the lxml element object
        #         buyers_element = tree.xpath(xpath_expression)[0]
        #
        #         # Extract text content from the lxml element object
        #         cusip_number = buyers_element.text_content().strip()
        #
        #         if cusip_number:
        #             return cusip_number
        #         else:
        #
        #             # Construct the search URL
        #             url = f"http://www.quantumonline.com/search.cfm?tickersymbol={ticker}&sopt=symbol"
        #
        #             try:
        #                 # Attempt to fetch the page
        #                 response = requests.get(url, timeout=10)  # Added timeout for the request
        #                 # Check if the request was successful
        #                 response.raise_for_status()
        #             except requests.RequestException as e:
        #                 print(f"Failed to retrieve page: {e}")
        #                 return None
        #
        #             try:
        #                 # Parse the HTML content
        #                 tree = html.fromstring(response.content)
        #                 # Define the XPath to locate the CUSIP number text
        #                 xpath = "//center[b[contains(text(), 'CUSIP:')]]"
        #                 # Attempt to extract the CUSIP number using the XPath
        #                 cusip_element = tree.xpath(xpath)
        #                 if cusip_element :
        #                     # Extract the content and split to remove the exchange part
        #                     cusip_text = cusip_element[0].text_content().split("Exchange")[0]
        #                     # Further split to isolate the CUSIP number
        #                     cusip_number = cusip_text.split("CUSIP:")[-1].strip()
        #                     return cusip_number
        #
        #                 else:
        #                     return None
        #             except Exception as e:
        #     # Handle unexpected parsing errors
        #                 print(f"Error extracting CUSIP number: {e}")
        #                 return None
        #
        #
        #     except IndexError:
        #         print("CUSIP number not found in the page.")
        #
        # except Exception as e:
        #     # Handle unexpected parsing errors
        #     print(f"Error extracting CUSIP number: {e}")
        #     return None
def parallel_fetch_cusips(client_df, ticker_col, cusip_col):
    def fetch_cusip_from_ticker(ticker):
        processor = FormulaDataProcessor()
        ids = [ticker]
        display_names = ["cusip"]
        timeSeries_formulas = ["FF_CUSIP(CURR)"]
        price_as_on_date = datetime(2024, 6, 30)
        as_on_date = price_as_on_date.strftime("%m/%d/%Y")

        time_Series_df = processor.fetch_time_series_data(ids, timeSeries_formulas, display_names)

        return time_Series_df["cusip"][0]

    ### changes
    cusips = client_df[cusip_col].tolist()

    def extract_ticker(ticker_value):
        # Ensure the ticker_value is a string
        ticker_str = str(ticker_value)
        # Split the string by both spaces and underscores
        components = re.split(r'[ _.]', ticker_str)
        # Assume the ticker is always the first part
        return components[0]

    for i in range(len(client_df)):
        if pd.isnull(client_df[cusip_col][i]) or client_df[cusip_col][i] == "":
            # Extract the ticker from the column
            ticker = extract_ticker(client_df[ticker_col][i])
            print("tllllllll:", ticker)
            # Simulate fetching CUSIP for each ticker
            cusip = fetch_cusip_from_ticker(ticker)
            client_df.loc[i, cusip_col] = cusip


give
me
multithreading