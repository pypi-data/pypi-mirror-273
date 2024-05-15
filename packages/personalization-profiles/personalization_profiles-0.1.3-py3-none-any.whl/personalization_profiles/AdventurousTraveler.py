from .PersonalizationProfile import PersonalizationProfile

class AdventurousTraveler(PersonalizationProfile):
    def __init__(self):
        super().__init__()

    def get_persona_description(self) -> None:
        prompt = f"""I'm {self.get_name()}, seeking thrills and adventures around every corner. 
        My assistant assists in planning travel that's off the beaten path, finding airlines and accommodations that get me close to nature and adventure sports. 
        We focus on destinations known for outdoor activities like hiking, surfing, and skydiving. Safety gear, local guides, and the best spots for adrenaline-pumping activities are on our checklist. 
        Flight dates and times are flexible to accommodate the best seasons for activities, as {self.get_time_preference()}, and I'm open to {self.get_class_preference()} as long as it gets me to my next adventure. """
        return prompt