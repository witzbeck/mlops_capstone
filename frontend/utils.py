from streamlit import error, json, success


def process_response(response):
    """
    Utility function to process the API response.

    Args:
    response (requests.Response): The response object from requests.post or requests.get.

    Description:
    This function checks the HTTP status code of the response. If the status code indicates success (200),
    it will parse the JSON response and display the extracted data using streamlit's json method.
    If the status code indicates an error, it will display an error message in the Streamlit app using
    streamlit's error method.
    """
    if response.status_code == 200:
        try:
            # Attempt to convert the response content to JSON
            extracted_data = response.json()
            success("Data extracted successfully!")
            # Display the JSON formatted data
            json(extracted_data)
        except ValueError:
            # Handle the case where JSON conversion fails
            error("Failed to parse the response as JSON.")
    else:
        # Display an error message with the HTTP status and the reason
        error(
            f"Failed to extract data. Status code: {response.status_code} - {response.reason}"
        )
