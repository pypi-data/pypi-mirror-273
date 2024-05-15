from .PersonalizationProfile import PersonalizationProfile
from langchain.prompts import PromptTemplate

class EcoTraveler(PersonalizationProfile):
    def __init__(self) -> None:
        super().__init__()


    def get_persona_description(self) -> None:
        
        prompt = f"""I'm {self.get_name()} passionate about protecting the environment. 
        Help me make eco-friendly choices when making travel plans and when I travel. 
        The assistant helps me find the routes, airlines, and accommodation options with the lowest carbon footprint. 
        It also provides me with tips on how to reduce my carbon footprint during and after my flight. 
        With the help of the Eco-Flight Assistant, I can travel without leaving a big impact on the planet. 
        Flight dates and hours are important for me. {self.get_time_preference()} {self.get_class_preference()}. """

        return prompt

    