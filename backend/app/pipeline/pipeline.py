import psycopg2
from dotenv import load_dotenv
import os

from fetch_fpl import fetch_bootstrap
from fetch_fpl import fetch_fixtures

from transform_fpl import transform_fixtures
from transform_fpl import transform_players
from transform_fpl import transform_teams

from load_fpl import load_fixtures
from load_fpl import load_players
from load_fpl import load_teams

load_dotenv()


def run_pipeline():
    connection = psycopg2.connect(os.getenv("DATABASE_URL_port6543_transaction_pooler"))


    bootstrap_data_raw = fetch_bootstrap()
    fixture_data_raw   = fetch_fixtures()

    teams_data_transformed   = transform_teams(bootstrap_data_raw)
    player_data_transformed  = transform_players(bootstrap_data_raw)
    fixture_data_transformed = transform_fixtures(fixture_data_raw)

    # MUST BE IN THE ORDER 
    # team FIRST, then players and fixtures. both of these depend on teams

    load_teams(teams_data_transformed, connection)
    load_players(player_data_transformed, connection)
    load_fixtures(fixture_data_transformed, connection)

    connection.close()

if __name__ == "__main__":
    run_pipeline()
