import re
from enum import Enum
from typing import List, Protocol

# 🎭🎯💡💪🏔🕮👊🏹🎓🎱📿🟋🗲🗰💥🔾🦉🧪🧠🧘🔮🔬🧫⚗🎔◉●⚆⬢⬣⬤⬆⚇

class Ability(Enum):
    STR = '💪' # reddy brown
    DEX = '🎯' # green
    CON = '🏔' # black
    WIS = '🦉' # purple
    INT = '🎓' # blue, studious
    CHA = '🎭' # yellow

    def __str__(self):
        return self.value

class AbilityRequirement(Enum):
    MAJOR_STR = [Ability.STR, Ability.STR]
    MINOR_STR = [Ability.STR]
    MAJOR_DEX = [Ability.DEX, Ability.DEX]
    MINOR_DEX = [Ability.DEX]
    MAJOR_CON = [Ability.CON, Ability.CON]
    MINOR_CON = [Ability.CON]
    MAJOR_WIS = [Ability.WIS, Ability.WIS]
    MINOR_WIS = [Ability.WIS]
    MAJOR_INT = [Ability.INT, Ability.INT]
    MINOR_INT = [Ability.INT]
    MAJOR_CHA = [Ability.CHA, Ability.CHA]
    MINOR_CHA = [Ability.CHA]
    ANY = []

    def __str__(self):
        return "-".join(reversed(self.name.split('_'))).lower()

class StatWithValue:
    stat = None
    value = None
    unit = None

    def __init__(self, stat: str, value: str, unit: str = None):
        self.stat = stat
        self.value = value
        self.unit = unit


class ActionCost:
    def __init__(self, action: int = 0, reaction: int = 0):
        self.action = action
        self.reaction = reaction
        if (self.reaction + self.action) <= 0:
            raise TypeError("Action must cost at least 1 Action or Reaction")
        
    def __str__(self):
        return "".join(["🔾"] * self.action + ["🗲"] * self.reaction)

class CastingDuration(Enum):
    INSTANTANEOUS = 1
    CONCENTRATION = 2
    ROUNDS = 3
    DESCRIPTION = 4

    def __str__(self):
        return self.name.title()


class Actionable(Protocol):
    action_cost: ActionCost

class Castable(Protocol):
    casting_duration: CastingDuration

class Image:
    mime_type: str
    base64_data: str

    def __init__(self, mime_type: str = "png", base64_data: str = "iVBORw0KGgoAAAANSUhEUgAAAD8AAAAhCAIAAADh4eRjAAABhWlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw1AUhU9bpUUqDlYQcchQXbRQVMRRq1CECqFWaNXB5KV/0KQhSXFxFFwLDv4sVh1cnHV1cBUEwR8QNzcnRRcp8b6k0CLGC4/3cd49h/fuA/yNClPNrjigapaRTiaEbG5VCL4iBB8GMIa4xEx9ThRT8Kyve+qluovxLO++P6tXyZsM8AnEs0w3LOIN4ulNS+e8TxxhJUkhPiceN+iCxI9cl11+41x02M8zI0YmPU8cIRaKHSx3MCsZKvEUcVRRNcr3Z11WOG9xVis11ronf2E4r60sc53WMJJYxBJECJBRQxkVWIjRrpFiIk3nCQ//kOMXySWTqwxGjgVUoUJy/OB/8Hu2ZmFywk0KJ4DuF9v+GAGCu0Czbtvfx7bdPAECz8CV1vZXG8DMJ+n1thY9Avq2gYvrtibvAZc7wOCTLhmSIwVo+QsF4P2MvikH9N8CPWvu3FrnOH0AMjSr1A1wcAiMFil73ePdoc65/dvTmt8Pmqtyt9oCiM8AAAAJcEhZcwAALiMAAC4jAXilP3YAAAAHdElNRQflCAEVLgATe2SCAAAAGXRFWHRDb21tZW50AENyZWF0ZWQgd2l0aCBHSU1QV4EOFwAAADlJREFUWMPtzjENADAIADCYf4Oc/IiYDkiroFnTsdaLzezt7e3t7e3t7e3t7e3t7e3t7e3t7e1v7j8dGALo1+za6wAAAABJRU5ErkJggg=="):
        self.mime_type = mime_type
        self.base64_data = base64_data

class Labelled(Protocol):
    name: str
    type: str
    sub_type: str

    def label_type(self) -> str:
        raise NotImplementedError()

class Action:
    action_cost: ActionCost

    def __init__(self,
                 name: str,
                 type: str,
                 sub_type: str,
                 action_cost: ActionCost,
                 description: List[str],
                 stat_blocks: List[StatWithValue],
                 casting_duration: CastingDuration=None):
        self.name = name
        self.type = type
        self.sub_type = sub_type
        self.action_cost = action_cost
        self.sub_type = sub_type
        self.description = description
        self.stat_blocks = stat_blocks
        self.casting_duration = casting_duration

    def label_type(self) -> str:
        return self.type

class Card:
    name: str
    sub_type: str
    flavour: str = None
    description: List[str] = []
    grants_actions: List[Action]
    stat_blocks: List[StatWithValue] = []
    level_requirement: int = 1
    special_quote: str = None
    feature_image: Image = None
    full_image: Image = None


    def __init__(self,
                 name: str,
                 type: str,
                 sub_type: str,
                 ability_requirement: AbilityRequirement = AbilityRequirement.ANY,
                 level_requirement: int = 1,
                 flavour: str = None,
                 description: List[str] = None,
                 grants_actions: List[Action] = None,
                 stat_blocks: List[StatWithValue] = None,
                 **kwargs):
        self.name = name
        self.type = type
        self.sub_type = sub_type
        self.ability_requirement = ability_requirement
        self.level_requirement = level_requirement
        self.flavour = flavour
        self.description = description
        self.grants_actions = grants_actions
        self.stat_blocks = stat_blocks
        self.action_cost = kwargs.get("action_cost")
        self.special_quote = kwargs.get("special_quote", None)
        self.feature_image = kwargs.get("feature_image", Image())
        self.full_image = kwargs.get("full_image", None)
        self.ammo_type = kwargs.get("ammo_type", None)

    def label_type(self) -> str:
        return self.type