import requests

def fetch_bootstrap():
    bootstrap_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    
    try:
        bootstrap_response = requests.get(bootstrap_url)
        bootstrap_response.raise_for_status()
        return bootstrap_response.json()

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch bootstrap data: {e}")
        return None

def fetch_fixtures():
    fixture_url = "https://fantasy.premierleague.com/api/fixtures/"
    
    try:
        fixture_response = requests.get(fixture_url)
        fixture_response.raise_for_status()
        return fixture_response.json()

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch fixture data: {e}")
        return None
        

if __name__ == "__main__":
    import requests

    bootstrap = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
    print(list(bootstrap.keys()))

    fixtures = requests.get("https://fantasy.premierleague.com/api/fixtures/").json()
    print(type(fixtures))
    print(fixtures[0].keys())