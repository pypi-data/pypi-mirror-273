
class User():
    def __init__(self, name=None) -> None:
        """
        Initialize a Person object.

        Args:
            name (str): The person's name.
            preferences (dict): The person's preferences for personalization.
            is_introduced (bool): Indicates whether the person has been introduced.

        Returns:
            None
        """
        self.name = name

    def set_profile(self,user_profile:dict) -> None:
        """
        Sets the user's profile information.

        Args:
            user_profile (dict): A dictionary containing the user's profile information.

        Returns:
            None
        """
        self.name = user_profile["name"]
        
    def get_name(self) -> str:
        """
        Returns the name of the user.
        """
        return self.name
    