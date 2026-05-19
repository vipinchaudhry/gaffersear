from datetime import datetime
import time

def transform_teams(bootstrap_data_raw):
    # bootstrap_data_raw returns a dictionary. one of those keys is teams. 
    # the value of teams is a list of dictionaries
    
    list_of_teams = bootstrap_data_raw["teams"]
    teams_data_transformed = []

    for team in list_of_teams:
        team_info = {
            "league_id"            : 1,
            "team_name"            : team["name"],
            "short_name"           : team["short_name"],
            "fpl_team_id"          : team["id"],
            "fpl_team_code"        : team["code"],
            "strength_overall_home": team["strength_overall_home"],
            "strength_overall_away": team["strength_overall_away"],
            "strength_attack_home" : team["strength_attack_home"],
            "strength_attack_away" : team["strength_attack_away"],
            "strength_defence_home": team["strength_defence_home"],
            "strength_defence_away": team["strength_defence_away"]
        }

        teams_data_transformed.append(team_info)

    return teams_data_transformed #this is a list of dictionaries



def transform_players(bootstrap_data_raw):
    # bootstrap_data_raw returns a dictionary
    # one of those keys is elements (this refers to players, but its called elements for some reason)
    # other keys realted to this is element_stats, element_types

    list_of_players = bootstrap_data_raw["elements"]
    player_data_transformed = []

    for player in list_of_players:

        if player["element_type"] == 1:
            player_position = "GKP"
        elif player["element_type"] == 2:
            player_position = "DEF"
        elif player["element_type"] == 3:
            player_position = "MID"
        elif player["element_type"] == 4:
            player_position = "FWD"
        else:
            player_position = "NA"


        player_info = {
            "team_id"                     : player["team"], # will be resolved in load_fpl
            "player_name"                 : player["first_name"] + " " + player["second_name"],
            "known_name"                  : player["web_name"],
            "position"                    : player_position,
            "fpl_player_id"               : player["id"],
            "player_status"               : player["status"],
            "chance_of_playing_this_round": player["chance_of_playing_this_round"],
            "chance_of_playing_next_round": player["chance_of_playing_next_round"],
            "news"                        : player["news"],
            "form"                        : float(player["form"]),
            "points_per_game"             : float(player["points_per_game"]),
            "total_points"                : float(player["total_points"]),
            "now_cost"                    : float(player["now_cost"]) / 10,
            "selected_by_percent"         : float(player["selected_by_percent"]),
            "expected_goals"              : float(player["expected_goals"]),
            "expected_assists"            : float(player["expected_assists"]),
            "expected_goal_involvements"  : float(player["expected_goal_involvements"]),
            "expected_goals_conceded"     : float(player["expected_goals_conceded"])
        }

        player_data_transformed.append(player_info)
    
    return player_data_transformed # this is a list of dictionaries

def transform_fixtures(fixtures_data_raw):
    # fixtures_data_raw is a list of dictionaries.
    # writing for fixture in fixtures_data_raw -> each fixture is a dictionary
    # we return another list of dictionaries fixture_data_transformed


    fixtures_data_transformed = []
    

    for fixture in fixtures_data_raw:
        # loop through each fixture and check if status
        # then get rest of the values 
        # append to the list

        if fixture["started"] == False:
            fixture_status_variable = "scheduled"
        elif (fixture["started"] == True and fixture["finished"] == False):
            fixture_status_variable = "in progress"
        elif (fixture["finished"] == True):
            fixture_status_variable = "finished"
        else:
            fixture_status_variable = "unknown"

        # normally here we would load the teams table first then make it do a lookup
        # for the home/away team_id but this is a solo project so we are doing this way
        # wtv
        fixture_info = {
                "league_id"      : 1, #hardcoded rn because there is only PL
                "home_team_id"   : fixture["team_h"], # this is FPL team id, not DB team id
                "away_team_id"   : fixture["team_a"], # this is resolved in load_fpl.py
                "gameweek"       : fixture["event"],
                "match_date"     : fixture["kickoff_time"],
                "home_difficulty": fixture["team_h_difficulty"],
                "away_difficulty": fixture["team_a_difficulty"],
                "home_score"     : fixture["team_h_score"],
                "away_score"     : fixture["team_a_score"],
                "fixture_status" : fixture_status_variable,
                "fpl_fixture_id" : fixture["id"]
            }

        fixtures_data_transformed.append(fixture_info)
    
    return fixtures_data_transformed # this is a list of dictionaries



if __name__ == "__main__":
    from fetch_fpl import fetch_bootstrap
    from fetch_fpl import fetch_fixtures

    import pprint
    

    bootstrap_data_raw = fetch_bootstrap()
    fixtures_data_raw   = fetch_fixtures()

    pprint.pprint(transform_teams(bootstrap_data_raw)[:2])
    pprint.pprint(transform_players(bootstrap_data_raw)[:2])
    pprint.pprint(transform_fixtures(fixtures_data_raw)[:2])

