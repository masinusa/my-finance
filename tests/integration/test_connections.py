import requests


def test_db_connector():
    """ Test container reachability
    """
    # Create a test client using the Flask application configured for testing
    try:
        response = requests.get("http://db_connector:5000/")
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError("Connection error, check container is running or URL is correct.")
    assert response.ok
    assert 'DB_Connector Container is Running' in response.text

def test_manager():
    """ Test container reachability
    """
    # Create a test client using the Flask application configured for testing
    try:
        response = requests.get('http://manager:5000/')
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError("Connection error, check container is running or URL is correct.")
    assert response.ok
    assert 'Manager Container is Running' in response.text

def test_plaid():
    """ Test container reachability
    """
    # Create a test client using the Flask application configured for testing
    try:
        response = requests.get('http://plaid:5000/')
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError("Connection error, check container is running or URL is correct.")
    assert response.ok
    assert 'Plaid API Container is Running' in response.text
