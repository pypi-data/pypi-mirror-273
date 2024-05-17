import json
from pathlib import Path
from typing import List

CURRENT_DIR = Path(__file__).parent
cities = json.load(open(CURRENT_DIR / "cities.json"))


def get_cities(state: str) -> List[str]:
    if state not in cities:
        return []
    return cities[state]


if __name__ == "__main__":
    print(get_cities("New York"))  # ['Los Angeles', 'San Francisco', 'San Diego']
