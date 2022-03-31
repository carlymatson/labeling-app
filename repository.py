import uuid
import random


def random_request(seed: int = 0):
    prefixes = [
        "The caller states that there is",
        "There is",
        "He state there is",
        "She says that there is",
    ]
    items = [
        "horse",
        "banana",
        "pothole",
        "leak",
        "power outage",
        "radioactive can of soup",
        "stop sign",
    ]
    connectors = ["in the", "in front of the", "falling into the"]
    location = [
        "road",
        "sewer",
        "toilet",
        "Wendy's",
        "wires",
        "trees",
        "sidewalk",
        "storm drain",
    ]
    # random.random.seed(seed)
    prefix = random.choice(prefixes)
    item = random.choice(items)
    connector = random.choice(connectors)
    location = random.choice(location)
    description = f"{prefix} a {item} {connector} {location}"
    return (uuid.uuid4(), description)


class Repository:
    def get_request_to_label(self, session_tag: str = ""):
        id = uuid.uuid4()
        description = "There is a horse in the road and it is eating all of my shoes"
        return id, description

    def get_batch(self, batch_size=10, session_tag: str = "", labeler_id: str = ""):
        return [random_request(i) for i in range(batch_size)]

    def propose_batch(self):
        pass
