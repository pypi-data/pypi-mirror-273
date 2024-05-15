class Alley:
    """
    Represents a bowling alley where games are played, including details about the lane conditions.

    Attributes:
        name (str): The name of the alley.
        location (str): The geographic location of the alley.
        lane_type (str): The type of lane surface, such as 'Wood' or 'Synthetic'.
    """

    VALID_LANE_TYPES = {'wood', 'synthetic'}

    def __init__(self, name: str, location: str, lane_type: str):
        """
        Initialize a new Alley instance.

        Parameters:
            name (str): The name of the alley.
            location (str): The geographic location of the alley.
            lane_type (str): The type of lane surface, indicating the material of the bowling lane.

        Raises:
            ValueError: If lane_type is not 'Wood' or 'Synthetic'.
        """
        self.name = name
        self.location = location
        if lane_type.lower() not in self.VALID_LANE_TYPES:
            raise ValueError(f"Invalid lane type '{lane_type}'. Valid types are: 'Wood', 'Synthetic'")
        self.lane_type = lane_type.capitalize()

    def __str__(self):
        """
        Return a string representation of the Alley instance, which is helpful for debugging and logging.

        Returns:
            str: A string that represents this Alley.
        """
        return f"{self.name} - {self.location} ({self.lane_type})"


if __name__ == "__main__":
    alley = Alley("Strike Zone", "Downtown", "Synthetic")
    print(alley)
