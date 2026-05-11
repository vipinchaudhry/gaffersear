CREATE INDEX IF NOT EXISTS idx_teams_league_id ON teams(league_id);

CREATE INDEX IF NOT EXISTS idx_players_team_id ON players(team_id);

CREATE INDEX IF NOT EXISTS idx_fixtures_league_id ON fixtures(league_id);
CREATE INDEX IF NOT EXISTS idx_fixtures_home_team_id ON fixtures(home_team_id);
CREATE INDEX IF NOT EXISTS idx_fixtures_away_team_id ON fixtures(away_team_id);
CREATE INDEX IF NOT EXISTS idx_fixtures_match_date ON fixtures(match_date);

CREATE INDEX IF NOT EXISTS idx_player_stats_player_id ON player_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_player_stats_fixture_id ON player_stats(fixture_id);

CREATE INDEX IF NOT EXISTS idx_picks_player_id ON picks(player_id);
CREATE INDEX IF NOT EXISTS idx_picks_league_id ON picks(league_id);
CREATE INDEX IF NOT EXISTS idx_picks_gameweek ON picks(gameweek);

-- syntax pattern is idx_ + table_name + column_name
