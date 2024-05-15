
class User():
    def __init__(self, name=None, email=None) -> None:
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
        self.email = email


    def set_profile(self,user_profile:dict) -> None:
        """
        Sets the user's profile information.

        Args:
            user_profile (dict): A dictionary containing the user's profile information.

        Returns:
            None
        """
        self.name = user_profile["name"]
        self.email = user_profile["email"]
        
    def get_name(self) -> str:
        """
        Returns the name of the user.
        """
        return self.name
    
    def get_email(self) -> str:
        """
        Returns the email of the user.
        """
        return self.email
    