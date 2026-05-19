


def load_teams(teams_data_transformed, connection):
    cursor = connection.cursor()
    cursor.executemany("""
                    INSERT INTO teams (league_id, team_name, short_name, fpl_team_id, fpl_team_code, 
                                    strength_overall_home, strength_overall_away, 
                                    strength_attack_home, strength_attack_away, 
                                    strength_defence_home, strength_defence_away)
                    
                    VALUES (%(league_id)s, %(team_name)s, %(short_name)s, %(fpl_team_id)s, %(fpl_team_code)s, 
                            %(strength_overall_home)s, %(strength_overall_away)s, 
                            %(strength_attack_home)s, %(strength_attack_away)s, 
                            %(strength_defence_home)s, %(strength_defence_away)s)
                    
                    ON CONFLICT (fpl_team_id) DO UPDATE
                    
                    SET team_name            = EXCLUDED.team_name,
                        short_name            = EXCLUDED.short_name,
                        fpl_team_code         = EXCLUDED.fpl_team_code,
                        strength_overall_home = EXCLUDED.strength_overall_home,
                        strength_overall_away = EXCLUDED.strength_overall_away,
                        strength_attack_home  = EXCLUDED.strength_attack_home,
                        strength_attack_away  = EXCLUDED.strength_attack_away,
                        strength_defence_home = EXCLUDED.strength_defence_home,
                        strength_defence_away = EXCLUDED.strength_defence_away
                """, 
                teams_data_transformed)
    
    connection.commit()
    cursor.close()
    # we dont close the connection here. connection belongs to pipeline.py
    # closing here means we close the connection before the other functions run
    # we start the connection in pipeline.py so we close there also


def get_fpl_team_id_map(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT fpl_team_id, team_id FROM teams")
    rows = cursor.fetchall()  # returns a list of tuples: [(fpl_team_id, team_id), ...]
    cursor.close()
    return {row[0]: row[1] for row in rows}

def load_players(player_data_transformed, connection):

    tuples_pairing_of_ids = get_fpl_team_id_map(connection)

    cursor = connection.cursor()
    for player in player_data_transformed:
        player["team_id"] = tuples_pairing_of_ids[player["team_id"]]

    cursor.executemany("""
                    INSERT INTO players (team_id, player_name, known_name, position, fpl_player_id, player_status, 
                                        chance_of_playing_this_round, chance_of_playing_next_round, news, form, 
                                        points_per_game, total_points, now_cost, selected_by_percent, 
                                        expected_goals, expected_assists, 
                                        expected_goal_involvements, expected_goals_conceded)
                    
                    VALUES (%(team_id)s, %(player_name)s, %(known_name)s, %(position)s, %(fpl_player_id)s,%(player_status)s, 
                            %(chance_of_playing_this_round)s, %(chance_of_playing_next_round)s, %(news)s, %(form)s, 
                            %(points_per_game)s, %(total_points)s, %(now_cost)s, %(selected_by_percent)s, 
                            %(expected_goals)s, %(expected_assists)s, 
                            %(expected_goal_involvements)s, %(expected_goals_conceded)s)
                    
                    ON CONFLICT (fpl_player_id) DO UPDATE
                    
                    SET team_id                      = EXCLUDED.team_id,
                        player_name                  = EXCLUDED.player_name,
                        known_name                   = EXCLUDED.known_name,
                        position                     = EXCLUDED.position,
                        player_status                = EXCLUDED.player_status,
                        chance_of_playing_this_round = EXCLUDED.chance_of_playing_this_round,
                        chance_of_playing_next_round = EXCLUDED.chance_of_playing_next_round,
                        news                         = EXCLUDED.news,
                        form                         = EXCLUDED.form,
                        points_per_game              = EXCLUDED.points_per_game,
                        total_points                 = EXCLUDED.total_points,
                        now_cost                     = EXCLUDED.now_cost,
                        selected_by_percent          = EXCLUDED.selected_by_percent,
                        expected_goals               = EXCLUDED.expected_goals,
                        expected_assists             = EXCLUDED.expected_assists,
                        expected_goal_involvements   = EXCLUDED.expected_goal_involvements,
                        expected_goals_conceded      = EXCLUDED.expected_goals_conceded
                """, 
                player_data_transformed)
    
    connection.commit()
    cursor.close()

def load_fixtures(fixture_data_transformed, connection):

    cursor = connection.cursor()

    tuples_pairing_of_ids = get_fpl_team_id_map(connection)

    for fixture in fixture_data_transformed:
        fixture["home_team_id"] = tuples_pairing_of_ids[fixture["home_team_id"]]
        fixture["away_team_id"] = tuples_pairing_of_ids[fixture["away_team_id"]]

    cursor.executemany("""
                    INSERT INTO fixtures (league_id, home_team_id, away_team_id, gameweek, match_date, 
                                        home_difficulty, away_difficulty, home_score, away_score, 
                                        fixture_status, fpl_fixture_id)
                    
                    VALUES (%(league_id)s, %(home_team_id)s, %(away_team_id)s, %(gameweek)s, %(match_date)s, 
                            %(home_difficulty)s, %(away_difficulty)s, %(home_score)s, %(away_score)s, 
                            %(fixture_status)s, %(fpl_fixture_id)s)
                    
                    ON CONFLICT (fpl_fixture_id) DO UPDATE
                    
                    SET league_id       = EXCLUDED.league_id,
                        home_team_id    = EXCLUDED.home_team_id,
                        away_team_id    = EXCLUDED.away_team_id,
                        gameweek        = EXCLUDED.gameweek,
                        match_date      = EXCLUDED.match_date,
                        home_difficulty = EXCLUDED.home_difficulty,
                        away_difficulty = EXCLUDED.away_difficulty,
                        home_score      = EXCLUDED.home_score,
                        away_score      = EXCLUDED.away_score,
                        fixture_status  = EXCLUDED.fixture_status
                """, 
                fixture_data_transformed)
    
    connection.commit()
    cursor.close()










if __name__ == "__main__":
    import time
    from etl.utils.db_connection import get_engine
    from etl.extractors.weather_extractor import fetch_weather_data
    from etl.extractors.news_extractor import fetch_news_data
    from etl.extractors.stocks_extractor import fetch_stocks_data, TICKERS
    from etl.transformers.weather_transformer import transform_weather_current, transform_weather_forecast
    from etl.transformers.news_transformer import transform_news
    from etl.transformers.stocks_transformer import transform_stocks

    engine = get_engine()

    raw = fetch_weather_data()
    load_weather_current(transform_weather_current(raw), engine)
    load_weather_forecast(transform_weather_forecast(raw), engine)
    print("Weather data loaded successfully")

    for category in ["technology", "business", "science", "health"]:
        raw_news = fetch_news_data(category)
        load_news_data(transform_news(raw_news, category), engine)
        print(f"{category} news loaded successfully")

    for ticker in TICKERS:
        raw_stocks = fetch_stocks_data(ticker)
        load_stocks_data(transform_stocks(raw_stocks), engine)
        print(f"{ticker} loaded successfully")
        time.sleep(2)