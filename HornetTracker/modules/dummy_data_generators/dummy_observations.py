from HornetTracker.observations.models.observation import Observation
from HornetTracker.map.models.map import Map
from HornetTracker.jars.models.jar import Jar
import random
from copy import deepcopy
import time

# observation

# create an observation
class DummyObservationsGenerator:
    latitude = 50.9700
    longitude = 3.7331
    average_distance = 120
    heading = 10

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
        random_distance= [10,20,10,30,40,55,40]
        random_heading = [5,4,6,8,9,-7,-8,-5]
        result_latitude = cls.latitude
        result_longitude = cls.longitude
        result_average_distance = cls.average_distance
        result_heading = cls.heading
        cls.latitude += random.choice(random_values)
        cls.longitude += random.choice(random_values)
        cls.average_distance += random.choice(random_distance)
        cls.heading += random.choice(random_heading)
        return cls(round(result_latitude,6), round(result_longitude, 6), result_average_distance, result_heading)

    @classmethod
    def _return_as_dict(cls):
        return cls.__class__

    def __init__(self, latitude,
                 longitude,
                 average_distance,
                 heading):
        self.latitude = latitude
        self.longitude = longitude
        self.average_distance = average_distance
        self.heading = heading

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"latitude: {self.latitude}," \
               f"longitude:{self.longitude}," \
               f"average_distance: {self.average_distance}," \
               f"heading:{self.heading}"


new_obs = []

dummyobservations = DummyObservationsGenerator.generate(10)

for item in dummyobservations:
    print(item)
    print(item.__dict__)
    new_obs_dict = deepcopy(item.__dict__)
    new_obs.append(new_obs_dict)

print(new_obs)

for observation in new_obs:
    new__obs = Observation(**observation)
    new__obs.create()
#get a list of database items
myobservations = Observation.list()
# create first a dummy map with only a name
dummy_map = Map.create_map_without_latlng("Observations")
# create a folium map object with long lat
folium_map = dummy_map.generate_map(latitude=new_obs[0]["latitude"],
                                    longitude=new_obs[0]["longitude"])
# create observation markers for that map.
for observation in new_obs:
    Map.generate_map_marker(parent_map=folium_map,
                            observation=True,
                            latitude=observation["latitude"],
                            longitude=observation["longitude"],
                            average_distance=observation["average_distance"],
                            heading=observation["heading"])

if isinstance(folium_map._repr_html_(), str):
    print("generated string for folium map observation")
# print(folium_map._repr_html_())


