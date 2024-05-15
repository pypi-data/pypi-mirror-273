import numpy as np


# import traveller classes
from .PersonaType import PersonaType
from .AdventurousTraveler import AdventurousTraveler
from .BudgetTraveler import BudgetTraveler
from .BusinessTraveler import BusinessTraveler
from .EcoTraveler import EcoTraveler
from .FamilyTraveler import FamilyTraveler

# number of questions used in personalization survey to determine persona
PERSONA_SURVEY_LIMIT = 6

class PersonaManager():
    def __init__(self,user_data:dict, preferences:str) -> None:
        self.user_data = user_data
        self.Persona = None
        self.preferences = list(map(lambda x:int(x),list(preferences)))
        self.get_personalization_profile()

    def set_persona(self) -> str:
        """
        Maps the user's travel preferences to a predefined persona.
        Possible return values are 
        "BusinessTraveler", "BudgetTraveler", "FamilyTraveler", "AdventurousTraveler", "EcoTraveler"
        """

        weights = np.array([
            [0.21, 0.188, 0.034, 0.236, 0.127],
            [0.086, 0.25, 0.057, 0.245, 0.176],
            [0.257, 0.175, 0.287, 0.094, 0.176],
            [0.105, 0.088, 0.149, 0.094, 0.265],
            [0.257, 0.075, 0.276, 0.075, 0.118],
            [0.086, 0.225, 0.195, 0.255, 0.137]
        ])

        preferences_array = np.array(self.preferences)[:PERSONA_SURVEY_LIMIT].reshape(1, -1)

        # Multiply the matrices
        result = np.dot(weights.T, preferences_array.T)
        # Get the index of the maximum value
        max_index = np.argmax(result)

        personas = list(PersonaType)
        selected_persona = personas[max_index]
        self.persona_type = selected_persona

    def get_personalization_profile(self) -> None:
        #set persona type
        self.set_persona()
        if self.persona_type == PersonaType.BusinessTraveler:
            self.Persona = BusinessTraveler()  
        elif self.persona_type == PersonaType.BudgetTraveler:
            self.Persona = BudgetTraveler()
        elif self.persona_type == PersonaType.FamilyTraveler:
            self.Persona = FamilyTraveler()
        elif self.persona_type == PersonaType.AdventurousTraveler:
            self.Persona = AdventurousTraveler()
        elif self.persona_type == PersonaType.EcoTraveler:
            self.Persona = EcoTraveler()
        # record the time preferences and user data
        self.Persona.set_profile(self.user_data)
        self.Persona.persona_type = self.persona_type
        self.Persona.set_preferences(self.preferences)
        