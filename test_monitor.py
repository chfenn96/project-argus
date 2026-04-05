import pytest
from unittest.mock import patch
from requests.exceptions import ConnectionError
from monitor import check_uptime

# Test 1: What happens when the website is UP?
@patch('monitor.requests.get')
def test_check_uptime_success(mock_get):
    # Setup the fake network response
    mock_get.return_value.status_code = 200
    mock_get.return_value.ok = True
    
    # Run our function
    result = check_uptime("https://www.google.com")
    
    # Assert (verify) the output is what we expect
    assert result['status'] == 'UP'
    assert result['status_code'] == 200
    assert result['url'] == "https://www.google.com"

# Test 2: What happens when the website is DOWN/fails to connect?
@patch('monitor.requests.get')
def test_check_uptime_failure(mock_get):
    # Setup the fake network response to throw an error
    mock_get.side_effect = ConnectionError("Simulated Connection Error")
    
    # Run our function
    result = check_uptime("https://this-website-is-fake-and-will-fail.com")
    
    # Assert (verify) it handled the failure gracefully
    assert result['status'] == 'DOWN'
    assert result['status_code'] is None