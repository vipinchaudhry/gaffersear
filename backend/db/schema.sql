-- 1. leagues
CREATE TABLE IF NOT EXISTS leagues (
    league_id   SERIAL PRIMARY KEY,
    league_name VARCHAR(100) NOT NULL,
    code        VARCHAR(10) NOT NULL UNIQUE,
    country     VARCHAR(100),
    created_at  TIMESTAMP DEFAULT NOW()
);

-- 2. teams

CREATE TABLE IF NOT EXISTS teams (
    team_id         SERIAL PRIMARY KEY,
    league_id       INTEGER REFERENCES leagues(league_id),
    team_name       VARCHAR(100) NOT NULL,
    short_name      VARCHAR(10),
    fpl_team_id     INTEGER UNIQUE,    -- maps to FPL API, nullable
    external_id     INTEGER,           -- football-data.org ID
    created_at      TIMESTAMP DEFAULT NOW()
);

-- 3. players

CREATE TABLE IF NOT EXISTS players (
    player_id       SERIAL PRIMARY KEY,
    team_id         INTEGER REFERENCES teams(team_id),
    player_name     VARCHAR(100) NOT NULL,
    position        VARCHAR(3),   -- GKP, DEF, MID, FWD
    fpl_player_id   INTEGER UNIQUE,   -- nullable, PL only
    external_id     INTEGER,          -- football-data.org ID
    is_available    BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- 4. fixtures

CREATE TABLE IF NOT EXISTS fixtures (
    fixture_id      SERIAL PRIMARY KEY,
    league_id       INTEGER REFERENCES leagues(league_id),
    home_team_id    INTEGER REFERENCES teams(team_id),
    away_team_id    INTEGER REFERENCES teams(team_id),
    gameweek        INTEGER,
    match_date      TIMESTAMP,
    home_difficulty INTEGER,   -- 1-5 scale
    away_difficulty INTEGER,  -- 1-5 scale
    home_score      INTEGER,   -- null until played
    away_score      INTEGER,   -- null until played
    fixture_status  VARCHAR(20) DEFAULT 'scheduled',  -- scheduled, live, finished
    created_at      TIMESTAMP DEFAULT NOW()
);

-- 5. player_stats

CREATE TABLE IF NOT EXISTS player_stats (
    player_stat_id  SERIAL PRIMARY KEY,
    player_id       INTEGER REFERENCES players(player_id),
    fixture_id      INTEGER REFERENCES fixtures(fixture_id),
    goals           INTEGER DEFAULT 0,
    assists         INTEGER DEFAULT 0,
    minutes_played  INTEGER DEFAULT 0,
    yellow_cards    INTEGER DEFAULT 0,
    red_cards       INTEGER DEFAULT 0,
    form_score      DECIMAL(5,2),   -- calculated by pipeline
    created_at      TIMESTAMP DEFAULT NOW(),

    UNIQUE(player_id, fixture_id)   -- one row per player per game
);

-- 6. picks

CREATE TABLE IF NOT EXISTS picks (
    picks_id               SERIAL PRIMARY KEY,
    player_id              INTEGER REFERENCES players(player_id),
    gameweek               INTEGER,
    league_id              INTEGER REFERENCES leagues(league_id),
    composite_score        DECIMAL(5,2),   -- the final weighted score
    form_component         DECIMAL(5,2),
    fixture_component      DECIMAL(5,2),
    availability_component DECIMAL(5,2),
    position               VARCHAR(3),
    created_at             TIMESTAMP DEFAULT NOW(),

    UNIQUE(player_id, gameweek)
);

-- 7. users

CREATE TABLE IF NOT EXISTS users (
    user_id     UUID PRIMARY KEY,    -- Supabase Auth user ID
    fpl_team_id INTEGER,             -- user's linked FPL team
    created_at  TIMESTAMP DEFAULT NOW()
);