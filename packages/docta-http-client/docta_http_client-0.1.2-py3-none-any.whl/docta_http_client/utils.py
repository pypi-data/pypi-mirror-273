import logging

def parse_json_response(response):
    """
    Parses JSON response and checks for errors in response.
    """
    try:
        data = response.json()
        if 'error' in data:
            logging.error(f"Error from API: {data['error']}")
            raise Exception(f"API Error: {data['error']}")
        return data
    except ValueError:
        raise ValueError("Invalid JSON received")

def check_status_code(response):
    """
    Check if the HTTP status code indicates an error and raise an exception if so.
    """
    if response.status_code != 200:
        logging.error(f"HTTP Error {response.status_code}: {response.text}")
        response.raise_for_status()
