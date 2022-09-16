from HornetTracker.observations.models.observation import Observation
from HornetTracker.map.models.map import Map
from HornetTracker.jars.models.jar import Jar
import random
from copy import deepcopy
import time


# observation

# create an observation
class DummyJarsGenerator:
    jar_name = None
    latitude = 50.9700
    longitude = 3.7331

    @classmethod
    def generate(cls, number_of_items: int) -> list:  # list of objects
        count = 1
        all_objects = []
        for count, i in enumerate(range(number_of_items), 1):
            time.sleep(1)
            dummy = cls._generate_next_observation()
            all_objects.append(dummy)
        print(count)
        # return a list of objects
        return all_objects

    @classmethod
    def _generate_next_observation(cls):
        random_values = [0.001, -0.002, -0.003, 0.004, -0.005, 0.006, -0.007, 0.008, 0.009]
        random_jar_names = [
            "Abra",
            "Absol",
            "Aerodactyl",
            "Aggron",
            "Aipom",
            "Alakazam",
            "Altaria",
            "Amaldo",
            "Ampharos",
            "Anorith",
            "Arbok",
            "Arcanine",
            "Ariados",
            "Aron",
            "Articuno",
            "Azumarill",
            "Azurill",
            "Bagon",
            "Baltoy",
            "Banette",
            "Barboach",
            "Bayleef",
            "Beautifly",
            "Beedrill",
            "Beldum",
            "Bellossom",
            "Bellsprout",
            "Blastoise",
            "Blaziken",
            "Blissey",
            "Breloom",
            "Bulbasaur",
            "Butterfree",
            "Cacnea",
            "Cacturne",
            "Camerupt",
            "Carvanha",
            "Cascoon",
            "Castform",
            "Caterpie",
            "Celebi",
            "Chansey",
            "Charizard",
            "Charmander",
            "Charmeleon",
            "Chikorita",
            "Chimecho",
            "Chinchou",
            "Clamperl",
            "Claydol",
            "Clefable",
            "Clefairy",
            "Cleffa",
            "Cloyster",
            "Combusken",
            "Corphish",
            "Corsola",
            "Cradily",
            "Crawdaunt",
            "Crobat",
            "Croconaw",
            "Cubone",
            "Cyndaquil",
            "Delcatty"]
        result_jar_name = cls.jar_name
        result_latitude = cls.latitude
        result_longitude = cls.longitude
        cls.jar_name = random.choice(random_jar_names)
        cls.latitude += random.choice(random_values)
        cls.longitude += random.choice(random_values)

        return cls(str(result_jar_name), round(result_latitude, 6), round(result_longitude, 6))

    @classmethod
    def _return_as_dict(cls):
        return cls.__class__

    def __init__(self, jar_name, latitude,
                 longitude):
        self.jar_name = jar_name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"jar_name: {self.jar_name}" \
               f"latitude: {self.latitude}," \
               f"longitude:{self.longitude}"


new_obs = []

dummy_jars = DummyJarsGenerator.generate(10)

for item in dummy_jars:
    print(item)
    print(item.__dict__)
    new_obs_dict = deepcopy(item.__dict__)
    new_obs.append(new_obs_dict)

print(new_obs)

for observation in new_obs:
    new__obs = Jar(**observation)
    new__obs.create()
# get a list of database items

myjars = Jar.list()

# create first a dummy map with only a name
dummy_map = Map.create_map_without_latlng("Observations")
# create a folium map object with long lat
folium_map = dummy_map.generate_map(latitude=new_obs[0]["latitude"],
                                    longitude=new_obs[0]["longitude"])
# create observation markers for that map.
for observation in new_obs:
    Map.generate_map_marker(parent_map=folium_map,
                            jar=True,
                            jar_name=observation["jar_name"],
                            latitude=observation["latitude"],
                            longitude=observation["longitude"])

if isinstance(folium_map._repr_html_(), str):
    print("generated string for folium map observation")
# print(folium_map._repr_html_())
