class Bowler:
    """
    Represents a bowler in a bowling simulation, including probabilities for striking and sparing,
    as well as personal characteristics like handedness and bowling technique.

    Attributes:
        name (str): The name of the bowler.
        strike_prob (float): Probability of hitting a strike.
        spare_prob (float): Probability of hitting a spare.
        handedness (str): The preferred hand of the bowler, either 'left' or 'right'.
        technique (str): The bowling technique used, either 'single' or 'double' handed.
    """

    def __init__(self, name: str, strike_prob: float, spare_prob: float, handedness: str = 'right', technique: str = 'single'):
        """
        Initializes a new instance of Bowler.

        Parameters:
            name (str): The name of the bowler.
            strike_prob (float): Probability of hitting a strike, between 0 and 1.
            spare_prob (float): Probability of hitting a spare, between 0 and 1.
            handedness (str): The preferred hand of the bowler, either 'left' or 'right' (default 'right').
            technique (str): The bowling technique used by the bowler, either 'single' or 'double' handed (default 'single').

        Raises:
            ValueError: If strike_prob or spare_prob is greater than 1.
        """
        if not (0 <= strike_prob <= 1):
            raise ValueError(f"Invalid strike probability {strike_prob}. Must be between 0 and 1.")
        if not (0 <= spare_prob <= 1):
            raise ValueError(f"Invalid spare probability {spare_prob}. Must be between 0 and 1.")
        if handedness not in ['left', 'right']:
            raise ValueError(f"Invalid handedness '{handedness}'. Must be 'left' or 'right'.")
        if technique not in ['single', 'double']:
            raise ValueError(f"Invalid technique '{technique}'. Must be 'single' or 'double'.")

        self.name = name
        self.strike_prob = strike_prob
        self.spare_prob = spare_prob
        self.handedness = handedness
        self.technique = technique

    def __str__(self):
        """
        Returns a string representation of the Bowler instance.

        Returns:
            str: A string that includes all the attributes of the Bowler.
        """
        return (f"Bowler(Name: {self.name}, Strike Probability: {self.strike_prob}, "
                f"Spare Probability: {self.spare_prob}, Handedness: {self.handedness}, "
                f"Technique: {self.technique})")


if __name__ == "__main__":
    # Create a bowler and print the object
    test_bowler = Bowler("Alice Johnson", strike_prob=0.45, spare_prob=0.55, handedness='left', technique='double')
    print(test_bowler)
