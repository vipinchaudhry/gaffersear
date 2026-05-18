import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((requests.exceptions.ConnectionError, requests.exceptions.Timeout)),
)
def fetch_bootstrap():
    bootstrap_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    
    
    bootstrap_response = requests.get(bootstrap_url)
    bootstrap_response.raise_for_status()
    return bootstrap_response.json()
    
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((requests.exceptions.ConnectionError, requests.exceptions.Timeout)),
)
def fetch_fixtures():
    fixture_url = "https://fantasy.premierleague.com/api/fixtures/"
    
    
    fixture_response = requests.get(fixture_url)
    fixture_response.raise_for_status()
    return fixture_response.json()
        

if __name__ == "__main__":

    bootstrap = fetch_bootstrap()
    print(list(bootstrap.keys()))

    fixtures = fetch_fixtures()
    print(type(fixtures))
    print(fixtures[0].keys())