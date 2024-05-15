from .PersonalizationProfile import PersonalizationProfile

class BudgetTraveler(PersonalizationProfile):
    def __init__(self):
        super().__init__()

    def get_persona_description(self) -> None:
        prompt = f"""I'm {self.get_name()}, always on the lookout for the best travel deals. 
        My assistant aids in finding the most cost-effective routes, airlines, and accommodations without compromising on quality. 
        We prioritize options that offer great value, such as budget airlines with good service. 
        Tips on saving money while in airports and flight experience. 
        Flight dates and times are based on the best deals, as {self.get_time_preference()}, and I usually go for {self.get_class_preference()} to keep travel costs low."""
        return prompt
    
    