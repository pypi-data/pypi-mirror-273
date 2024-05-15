from .User import User
import numpy as np
from langchain.prompts import PromptTemplate

class PersonalizationProfile(User):
    def __init__(self) -> None:
        """
        Initializes a new instance of the PersonalizationProfile class.

        Args:
            user_profile (dict): A dictionary containing user profile information.

        Returns:
            None
        """
        super().__init__(self)
        self.preferences = {}
        self.user_info = None
        self.persona_type = None
        self.persona_description = None
    
    def set_preferences(self, answers: list) -> None:
        """
        Sets the time preferences of the user.

        Parameters:
        - fly_weekdays: A boolean indicating whether the user prefers to fly on weekdays.
        - early_flights: A boolean indicating whether the user prefers early flights.

        Returns:
        None
        """
        # Convert the values of the preferences dictionary to booleans
        self.preferences["traveling alone"] = bool(answers[0])
        self.preferences["traveling with backpack"] = bool(answers[1])
        self.preferences["direct flights"] = bool(answers[2])
        self.preferences["eco friendly option"] = bool(answers[3])
        self.preferences["pay for more comfort"] = bool(answers[4])
        self.preferences["discovering new places"] = bool(answers[5])
        self.preferences["fly weekdays"] = bool(answers[6])
        self.preferences["early flights"] = bool(answers[7])

    def record_user_info(self, user_info: dict) -> None:
        """
        Records the user's personal information.

        Args:
            user_info (dict): A dictionary containing the user's personal information.

        Returns:
            None
        """
        self.user_info = user_info

    def pos_neg_constructor(self,feature,preference_or_need = "prefer"):
        if self.preferences[feature]:
            return f"{preference_or_need} {feature}"
        else:
            return f"do not {preference_or_need} {feature}"
    
    def get_time_preference(self) -> str:
        """
        Returns a string describing the user's time preferences.
        """
        connector = "but" if self.preferences['fly weekdays'] != self.preferences['early flights'] else "and" 
        return f"I {self.pos_neg_constructor('fly weekdays')} {connector} I {self.pos_neg_constructor('early flights')}."
    
    def get_class_preference(self) -> str:
        """
        Returns a string describing the user's luggage preferences.
        """
        prompt =  f"""I {self.pos_neg_constructor("traveling with backpack")} to travel with my backpack therefore \
            I {self.pos_neg_constructor("traveling with backpack"),"need"} to have a ticket class that offers high luggage limits."""
        prompt += f""" I {self.pos_neg_constructor('pay for more comfort')} to pay for more comfort therefore \
            I {self.pos_neg_constructor('pay for more comfort',"need")} higher flight class offering higher comfort."""
        return prompt