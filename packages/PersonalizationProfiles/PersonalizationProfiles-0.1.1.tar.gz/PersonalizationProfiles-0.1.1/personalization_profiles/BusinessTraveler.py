from .PersonalizationProfile import PersonalizationProfile

class BusinessTraveler(PersonalizationProfile):
    def __init__(self):
        super().__init__()


    def get_persona_description(self) -> None:
        prompt = f"""I'm {self.get_name()}, a business traveler focused on efficiency and comfort. 
        My assistant ensures my travel plans align with my schedule, selecting flights and accommodations that offer luxury and convenience. 
        {self.get_class_preference()} for my flights and value amenities that support productivity. 
        The assistant also helps me navigate between meetings and airports smoothly, prioritizing direct flights and expedited airport services. 
        Flight dates and hours are crucial. {self.get_time_preference()} is when I'm most likely to travel. """
        return prompt