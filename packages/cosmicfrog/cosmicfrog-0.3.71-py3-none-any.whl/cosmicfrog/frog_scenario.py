"""
    Helpers for manipulating Cosmic Frog scenarios
"""

from typing import List


## Does this need user to trigger or should it be automatic?
model.read_scenarios()

## This will trigger a read of all scenario tables
scenarios = FrogScenarioManager(model)

my_scenario = scenarios.add_scenario("scenario name")

my_scenario.add(Item("Name", condition="my condition", action="my action"))

scenario.delete_scenario()  # items will be orphaned, option to remove

scenarios.delete_scenario("xyz")

scenarios.delete_item("")


class FrogScenarioManager:
    """
    Helper class for manipulating Cosmic Frog model scenarios
    """

    def __init__(self, model) -> None:
        self.model = model

    def read_all(self):

        self.model.read_table("Scenarios")


class FrogScenarioItem:
    """
    Helper class for manipulating Cosmic Frog Scenario Items
    """


class FrogScenarioRule:
    """
    Helper class for manipulating Cosmic Frog Scenario Rules
    """

    def __init__(self) -> None:
        self.contents: List[FrogScenarioItem] = []


class FrogScenario:
    """
    Helper class for manipulating Cosmic Frog Scenarios
    """

    def __init__(self) -> None:
        self.contents: List[FrogScenarioItem | FrogScenarioRule] = []

    def add_item(self, item: FrogScenarioItem):
        """
        Add a scenario item to this scenario
        """
        self.contents.append(item)
        pass

    def remove_item(self, item: FrogScenarioItem):
        """
        Remove a scenario item from this scenario
        """
        pass
