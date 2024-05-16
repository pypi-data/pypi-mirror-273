import random
from enum import Enum
from typing import List, Dict

from car_model_fixtures.fixtures import cars


class Continent(Enum):
    EUROPE = 'Europe'


class FixtureGenerator:
    def __init__(self):
        self.cars = cars

    def generate(
            self,
            amount: int = 1,
            continent: Continent = Continent.EUROPE,
            year: int = 2023
    ) -> List[Dict[str, str]]:
        if amount <= 0:
            raise ValueError('You must generate at least one fixture')

        data = self.cars.get(continent.value, {}).get(str(year))
        if not data:
            raise ValueError('No data for given continent and year')

        fixtures = []
        for index in range(amount):
            brand, models = random.choice(list(data.items()))
            model = random.choice(models)
            fixtures.append({'brand': brand, 'model': model})

        return fixtures
