-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.

DROP DATABASE IF EXISTS tournamentdb;

CREATE DATABASE tournamentdb;

\c tournamentdb;

CREATE TABLE players (
player_id SERIAL,
player TEXT,
PRIMARY KEY (player_id));

CREATE TABLE matches (
match_id SERIAL,
won_player_id INTEGER REFERENCES players(player_id),
lost_player_id INTEGER REFERENCES players(player_id),
PRIMARY KEY (match_id));

CREATE VIEW standings AS
SELECT players.player_id, players.player, 
(SELECT count(matches.won_player_id) FROM matches 
WHERE players.player_id = matches.won_player_id) AS total_wins,
(SELECT count(matches.match_id) FROM matches
WHERE players.player_id = matches.won_player_id 
OR players.player_id = matches.lost_player_id) AS total_matches
FROM players
ORDER BY total_wins DESC;
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- (outside pqsl) Run it with: psql -f tournament.sql 
-- (inside pqsl) Run it with: \i tournament.sql
