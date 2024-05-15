import sqlite3
from typing import List, Tuple
from trueroll import Bowler, Alley


class BowlingDatabase:
    """
    Handles the storage and retrieval of bowling simulation data in an SQLite database.
    Provides methods to add and manage bowlers, alleys, games, and detailed game statistics.
    """

    def __init__(self, db_name: str = 'bowling.db'):
        """
        Initialises the database connection and creates tables if they do not already exist.

        Args:
            db_name (str): The filename of the database. Defaults to 'bowling.db'.
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_tables()

    def create_tables(self):
        """
        Creates tables in the database if they do not exist to store bowlers, alleys, games, and game details.
        """
        c = self.conn.cursor()

        # Create tables
        c.execute('''
        CREATE TABLE IF NOT EXISTS Bowlers (
            BowlerID INTEGER PRIMARY KEY,
            Name TEXT UNIQUE,
            Handedness TEXT,
            Style TEXT
        )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS Alleys (
            AlleyID INTEGER PRIMARY KEY,
            Name TEXT,
            Location TEXT,
            LaneType TEXT
        )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS OilPatterns (
            PatternID INTEGER PRIMARY KEY,
            Name TEXT,
            Description TEXT
        )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS Games (
            GameID INTEGER PRIMARY KEY,
            Date TEXT,
            AlleyID INTEGER,
            OilPatternID INTEGER,
            FOREIGN KEY (AlleyID) REFERENCES Alleys(AlleyID),
            FOREIGN KEY (OilPatternID) REFERENCES OilPatterns(PatternID)
        )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS GameDetails (
            GameID INTEGER,
            BowlerID INTEGER,
            FrameData TEXT,
            TotalScore INTEGER,
            StrikePercentage REAL,
            SparePercentage REAL,
            FOREIGN KEY (GameID) REFERENCES Games(GameID),
            FOREIGN KEY (BowlerID) REFERENCES Bowlers(BowlerID)
        )
        ''')

        # Commit changes
        self.conn.commit()

    def add_bowler(self, bowler: 'Bowler'):
        """
        Adds a new bowler to the database or updates an existing bowler with the same name.

        Args:
            bowler (Bowler): An instance of the Bowler class containing bowler data.

        Returns:
            int: The database ID of the added or updated bowler.
        """
        c = self.conn.cursor()
        c.execute('''
            INSERT INTO Bowlers (Name, Handedness, Style)
            VALUES (?, ?, ?) ON CONFLICT(Name) DO UPDATE SET
            Handedness=excluded.Handedness, Style=excluded.Style
        ''', (bowler.name, bowler.handedness, bowler.technique))
        self.conn.commit()
        return c.lastrowid

    def add_alley(self, alley: 'Alley'):
        """
        Adds a new bowling alley to the database.

        Args:
            alley (Alley): An instance of the Alley class containing alley data.

        Returns:
            int: The database ID of the added alley.
        """
        c = self.conn.cursor()
        c.execute('INSERT INTO Alleys (Name, Location, LaneType) VALUES (?, ?, ?)',
                  (alley.name, alley.location, alley.lane_type))
        self.conn.commit()
        return c.lastrowid

    def add_game(self, date: str, alley_id: int, oil_pattern_id: int, frames: List[Tuple[int, ...]]):
        """
        Adds a new game along with detailed frame data to the database.

        Args:
            date (str): The date the game was played.
            alley_id (int): The database ID of the alley where the game was played.
            oil_pattern_id (int): The database ID of the oil pattern used in the game.
            frames (List[Tuple[int, ...]]): A list of tuples representing the frames played in the game.
        """
        c = self.conn.cursor()
        c.execute('INSERT INTO Games (Date, AlleyID, OilPatternID) VALUES (?, ?, ?)', (date, alley_id, oil_pattern_id))
        game_id = c.lastrowid
        total_score, strike_percentage, spare_percentage = self.calculate_stats(frames)
        c.execute('''
            INSERT INTO GameDetails (GameID, FrameData, TotalScore, StrikePercentage, SparePercentage)
            VALUES (?, ?, ?, ?, ?)
        ''', (game_id, str(frames), total_score, strike_percentage, spare_percentage))
        self.conn.commit()

    def calculate_stats(self, frames: List[Tuple[int, ...]]) -> Tuple[int, float, float]:
        """
        Calculate total score, strike, and spare percentages from frame data.

        Args:
            frames (List[Tuple[int, ...]]): A list of tuples representing the frames played in the game.

        Returns:
            Tuple[int, float, float]: A tuple containing the total score, strike percentage, and spare percentage.
        """
        total_score = 0  # Implement scoring calculation based on rules
        strikes = sum(1 for frame in frames if frame[0] == 10)
        spares = sum(1 for frame in frames if sum(frame[:2]) == 10 and frame[0] != 10)
        total_frames = len(frames)
        strike_percentage = (strikes / total_frames) * 100
        spare_percentage = (spares / total_frames) * 100
        return total_score, strike_percentage, spare_percentage

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()


if __name__ == "__main__":
    # Example usage of the database class
    db = BowlingDatabase()
    # Here you might instantiate Bowler and Alley classes and add them using db.add_bowler() and db.add_alley()
    # This part would typically be extended to use actual data or more complex scenarios.
    print("Database setup complete.")
    db.close()
