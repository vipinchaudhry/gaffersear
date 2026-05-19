# Field Mapping

This document explains where the information comes from, what it represents, and the transformations applied.

## bootstrap-static

### Teams
Insert behaviour: DO NOTHING on fpl_team_id conflict.

| FPL Field | Database Column | Transformation |
|-----------|-----------------|----------------|
| (generated) | team_id | Automatic |
| (hardcoded) | league_id | Lookup PL row at insert time |
| name | team_name |  |
| short_name | short_name |  |
| id | fpl_team_id |  |
| code | fpl_team_code |  |
| strength_overall_home | strength_overall_home |  |
| strength_overall_away | strength_overall_away |  |
| strength_attack_home | strength_attack_home |  |
| strength_attack_away | strength_attack_away |  |
| strength_defence_home | strength_defence_home |  |
| strength_defence_away | strength_defence_away |  |


### Players
Upsert on fpl_player_id conflict.
Update all fields except player_id and created_at.

| FPL Field | Database Column | Transformation |
|-----------|-----------------|----------------|
| (generated) | player_id | Auto |
| elements[].team | team_id | Match fpl_team_id in teams, store internal team_id |
| first_name, second_name | player_name | string concatenation |
| web_name | known_name |  |  |
| element_type | position | 1→GKP, 2→DEF, 3→MID, 4→FWD |
| id | fpl_player_id |  |
| status | player_status |  |
| chance_of_playing_this_round | chance_of_playing_this_round |  |
| chance_of_playing_next_round | chance_of_playing_next_round |  |
| news | news |  |  |
| form | form | Cast string -> float |
| points_per_game | points_per_game | Cast string -> float |
| total_points | total_points |  |
| now_cost | now_cost | Divide by 10 -> store as float |
| selected_by_percent | selected_by_percent | Cast string -> float |
| expected_goals | expected_goals | Cast string -> float |
| expected_assists | expected_assists | Cast string -> float |
| expected_goal_involvements | expected_goal_involvements | Cast string -> float |
| expected_goals_conceded | expected_goals_conceded | Cast string -> float |
| auto | created_at | DB Default |
| auto | updated_at | DB Default |


### Fixtures

Upsert behavior: On fpl_fixture_id conflict UPDATE fixture_status, home_score, away_score, gameweek

| FPL Field | Database Column | Transformation |
|-----------|-----------------|----------------|
| (generated) | fixture_id | Auto |
| league_id | league_id | Lookup PL row at insert time |
| team_h | home_team_id | Lookup team_id on Teams table |
| team_a | away_team_id | Lookup team_id on Teams table |
| event | gameweek |  |
| kickoff_time | match_date |  |
| team_h_difficulty | home_difficulty |  |
| team_a_difficulty | away_difficulty |  |
| team_h_score | home_score |  |
| team_a_score | away_score |  |
| finished, started (bools) | fixture_status | AND/OR gates to determine scheduled, in_progress, finished |
| fixture_id | fpl_fixture_id |  |


### Events

| FPL Field | Used For | How |
|-----------|-----------------|----------------|
| id | gameweek_number | From Fixtures.gameweek and picks.gameweek |
| is_current | pipeline_logic | Identify which GW to sync — not stored |
| is_next | pipeline_logic | Identify upcoming GW for picks — not stored |
| finished | pipeline_logic | Skip fully finished GW if needed — not stored |
