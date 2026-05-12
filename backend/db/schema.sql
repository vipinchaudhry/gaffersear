-- 1. leagues
CREATE TABLE IF NOT EXISTS leagues (
    league_id    SERIAL PRIMARY KEY,
    league_name  VARCHAR(100) NOT NULL,
    code         VARCHAR(10) NOT NULL UNIQUE,  -- e.g. 'PL', 'BL1', 'PD'
    country      VARCHAR(100),
    created_at   TIMESTAMP DEFAULT NOW()
);

-- 2. teams
CREATE TABLE IF NOT EXISTS teams (
    team_id                  SERIAL PRIMARY KEY,
    league_id                INTEGER REFERENCES leagues(league_id),
    team_name                VARCHAR(100) NOT NULL,
    short_name               VARCHAR(10),
    fpl_team_id              INTEGER UNIQUE,   -- FPL API: teams[].id (changes each season)
    fpl_team_code            INTEGER UNIQUE,   -- FPL API: teams[].code (permanent, used in badge URLs)
    footballdata_team_id     INTEGER,          -- football-data.org team ID

    -- FPL strength ratings (used in scoring model)
    strength_overall_home    INTEGER,
    strength_overall_away    INTEGER,
    strength_attack_home     INTEGER,
    strength_attack_away     INTEGER,
    strength_defence_home    INTEGER,
    strength_defence_away    INTEGER,
    created_at               TIMESTAMP DEFAULT NOW()
);

-- 3. players
CREATE TABLE IF NOT EXISTS players (
    player_id                    SERIAL PRIMARY KEY,
    team_id                      INTEGER REFERENCES teams(team_id),
    player_name                  VARCHAR(100) NOT NULL,
    known_name                   VARCHAR(100),          -- FPL: known_name (e.g. "Salah" vs "Mohamed Salah")
    position                     VARCHAR(3),            -- GKP, DEF, MID, FWD (derived from element_type on insert)
    fpl_player_id                INTEGER UNIQUE,        -- FPL API: elements[].id
    footballdata_player_id       INTEGER,               -- football-data.org player ID

    -- Availability
    player_status                VARCHAR(1),            -- FPL: 'a' available, 'd' doubtful, 'i' injured, 's' suspended, 'u' unavailable
    chance_of_playing_this_round INTEGER,               -- FPL: 0-100, null means no concern
    chance_of_playing_next_round INTEGER,
    news                         TEXT,                  -- FPL injury/availability note e.g. "Knee injury, 75% chance"

    -- Form & scoring
    form                         NUMERIC(4,1),          -- FPL: rolling form score e.g. 6.5 (stored as string in API, cast on insert)
    points_per_game              NUMERIC(4,1),          -- FPL: average FPL points per game
    total_points                 INTEGER,               -- FPL: total FPL points this season

    -- Price
    now_cost                     NUMERIC(4,1),          -- FPL: price in £m e.g. 6.1 (API gives 61, divide by 10 on insert)

    -- Ownership
    selected_by_percent          NUMERIC(4,1),          -- FPL: % of FPL managers who own this player

    -- Expected stats (useful for ML model in V2)
    expected_goals               NUMERIC(6,2),
    expected_assists             NUMERIC(6,2),
    expected_goal_involvements   NUMERIC(6,2),
    expected_goals_conceded      NUMERIC(6,2),
    created_at                   TIMESTAMP DEFAULT NOW(),
    updated_at                   TIMESTAMP DEFAULT NOW()
);

-- 4. fixtures
CREATE TABLE IF NOT EXISTS fixtures (
    fixture_id              SERIAL PRIMARY KEY,
    league_id               INTEGER REFERENCES leagues(league_id),
    fpl_fixture_id          INTEGER UNIQUE,             -- FPL API: fixtures[].id (PL only, null for other leagues)
    footballdata_fixture_id INTEGER,                    -- football-data.org fixture ID
    home_team_id            INTEGER REFERENCES teams(team_id),
    away_team_id            INTEGER REFERENCES teams(team_id),
    gameweek                INTEGER,                    -- FPL: event id / matchday number
    match_date              TIMESTAMP,
    home_difficulty         INTEGER,                    -- FPL FDR: 1-5 scale
    away_difficulty         INTEGER,
    home_score              INTEGER,                    -- null until played
    away_score              INTEGER,
    fixture_status          VARCHAR(20) DEFAULT 'scheduled',  -- scheduled, live, finished
    created_at              TIMESTAMP DEFAULT NOW()
);

-- 5. player_stats
-- One row per player per fixture
CREATE TABLE IF NOT EXISTS player_stats (
    player_stat_id               SERIAL PRIMARY KEY,
    player_id                    INTEGER REFERENCES players(player_id),
    fixture_id                   INTEGER REFERENCES fixtures(fixture_id),

    -- Core stats
    minutes_played               INTEGER DEFAULT 0,
    goals                        INTEGER DEFAULT 0,
    assists                      INTEGER DEFAULT 0,
    clean_sheets                 INTEGER DEFAULT 0,     -- 1 if kept clean sheet, 0 if not
    goals_conceded               INTEGER DEFAULT 0,
    own_goals                    INTEGER DEFAULT 0,
    penalties_saved              INTEGER DEFAULT 0,
    penalties_missed             INTEGER DEFAULT 0,
    yellow_cards                 INTEGER DEFAULT 0,
    red_cards                    INTEGER DEFAULT 0,
    saves                        INTEGER DEFAULT 0,     -- GKP only
    bonus                        INTEGER DEFAULT 0,     -- FPL bonus points (0-3)
    bps                          INTEGER DEFAULT 0,     -- FPL bonus point system raw score

    -- Expected stats per fixture
    expected_goals               NUMERIC(6,2),
    expected_assists             NUMERIC(6,2),
    expected_goal_involvements   NUMERIC(6,2),
    expected_goals_conceded      NUMERIC(6,2),
    
    -- Calculated by pipeline
    form_score                   NUMERIC(5,2),
    created_at                   TIMESTAMP DEFAULT NOW(),

    UNIQUE(player_id, fixture_id)
);

-- 6. picks
CREATE TABLE IF NOT EXISTS picks (
    picks_id               SERIAL PRIMARY KEY,
    player_id              INTEGER REFERENCES players(player_id),
    gameweek               INTEGER NOT NULL,
    league_id              INTEGER REFERENCES leagues(league_id),
    composite_score        NUMERIC(5,2),
    form_component         NUMERIC(5,2),
    fixture_component      NUMERIC(5,2),
    availability_component NUMERIC(5,2),
    home_away_component    NUMERIC(5,2),               -- the 10% home/away factor from your scoring model
    position               VARCHAR(3),
    created_at             TIMESTAMP DEFAULT NOW(),

    UNIQUE(player_id, gameweek, league_id)             -- added league_id to unique constraint (same player could be picked across leagues)
);

-- 7. users
CREATE TABLE IF NOT EXISTS users (
    user_id     UUID PRIMARY KEY,   -- Supabase Auth user ID
    fpl_team_id INTEGER,            -- user's linked FPL team ID
    created_at  TIMESTAMP DEFAULT NOW()
);