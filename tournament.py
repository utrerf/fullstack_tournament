#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    DB = psycopg2.connect("dbname=tournamentdb")
    c = DB.cursor()
    return DB, c


def deleteMatches():
    """Remove all the match records from the database."""
    DB, c = connect()
    c.execute("TRUNCATE matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB, c = connect()
    c.execute("TRUNCATE players, matches;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB, c = connect()
    c.execute("SELECT count(*) FROM players;")
    result = c.fetchone()
    DB.close()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB, c = connect()
    QUERY = ("INSERT INTO players (player) VALUES (%s)")
    PARAMETERS = (name,)
    c.execute(QUERY, PARAMETERS)
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, c = connect()
    c.execute('''SELECT * FROM standings;''')
    result = c.fetchall()
    DB.commit()
    DB.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB, c = connect()
    QUERY = '''INSERT INTO matches (won_player_id, lost_player_id)
    VALUES (%s,%s)'''
    PARAMETERS = (winner, loser)
    c.execute(QUERY, PARAMETERS)
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    '''Please note that I looked at gringoirejyc solution to this problem
    in the forums after hours of not being able to find an elegant solution
    to the creation of the tupple here's the link to his post:
    https://discussions.udacity.com/t/problem-with-swisspairing-function
    /163329'''

    DB, c = connect()
    standings = playerStandings()
    player = [item[0:2] for item in standings]
    index = 0
    pairings = []
    while (index < len(standings)):
        pair = player[index]+player[index+1]
        pairings.append(pair)
        index = index + 2
    return pairings
    DB.close()
