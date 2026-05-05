-- USING (true);
-- means no row level filter (all rows visible)


-- Allow anon to read leagues
CREATE POLICY "anon can read leagues"
ON leagues
FOR SELECT
TO anon
USING (true);

-- Allow authenticated to read leagues

CREATE POLICY "authenticated can read leagues"
ON leagues
FOR SELECT
TO authenticated
USING (true); 

-----------------------------------------------------------------
-----------------------------------------------------------------
-----------------------------------------------------------------

-- Allow anon to read teams
CREATE POLICY "anon can read teams"
ON teams
FOR SELECT
TO anon
USING (true);

-- Allow authenticaed to read teams
CREATE POLICY "authenticated can read teams"
ON teams
FOR SELECT
TO authenticated
USING (true);

-----------------------------------------------------------------
-----------------------------------------------------------------
-----------------------------------------------------------------

-- Allow anon to read players
CREATE POLICY "anon can read players"
ON players
FOR SELECT
TO anon
USING (true);

-- Allow authenticaed to read players
CREATE POLICY "authenticated can read players"
ON players
FOR SELECT
TO authenticated
USING (true);

-----------------------------------------------------------------
-----------------------------------------------------------------
-----------------------------------------------------------------

-- Allow anon to read fixtures
CREATE POLICY "anon can read fixtures"
ON fixtures
FOR SELECT
TO anon
USING (true);

-- Allow authenticaed to read fixtures
CREATE POLICY "authenticated can read fixtures"
ON fixtures
FOR SELECT
TO authenticated
USING (true);

-----------------------------------------------------------------
-----------------------------------------------------------------
-----------------------------------------------------------------

-- Allow anon to read player_stats
CREATE POLICY "anon can read player_stats"
ON player_stats
FOR SELECT
TO anon
USING (true);

-- Allow authenticaed to read player_stats
CREATE POLICY "authenticated can read player_stats"
ON player_stats
FOR SELECT
TO authenticated
USING (true);

-----------------------------------------------------------------
-----------------------------------------------------------------
-----------------------------------------------------------------

-- Allow anon to read picks
CREATE POLICY "anon can read picks"
ON picks
FOR SELECT
TO anon
USING (true);

-- Allow authenticaed to read picks
CREATE POLICY "authenticated can read picks"
ON picks
FOR SELECT
TO authenticated
USING (true);

-----------------------------------------------------------------
-----------------------------------------------------------------
-----------------------------------------------------------------

-- ANON CANNOT DO ANYTHING TO USERS
-- no code here


-- Allow authenticaed to select, insert and update on their own row only
-- here INSERT and UPDATE use "WITH CHECK" not just "USING". Update gets both.

CREATE POLICY "authenticated can select own user row"
ON users
FOR SELECT
TO authenticated
USING (auth.uid() = user_id);

CREATE POLICY "authenticated can insert own user row"
ON users
FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "authenticated can update own user row"
ON users
FOR UPDATE
TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);