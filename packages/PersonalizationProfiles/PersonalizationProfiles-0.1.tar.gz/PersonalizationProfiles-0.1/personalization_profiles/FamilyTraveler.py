from .PersonalizationProfile import PersonalizationProfile

class FamilyTraveler(PersonalizationProfile):
    def __init__(self):
        super().__init__()


    def get_persona_description(self) -> None:
        prompt = f"""I'm {self.get_name()}, exploring the world with my family. 
        My assistant helps us find family-friendly travel options that cater to the needs of both adults and children. 
        We look for accommodations with amenities for kids, and transportation options that are convenient for family travel. 
        Safety, comfort, and fun activities nearby are our priorities. Flight dates and times are flexible, as {self.get_time_preference()}, and {self.get_class_preference()} to ensure comfort for the whole family."""
        return prompt