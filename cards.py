import re
from enum import Enum
from typing import List


class StatWithValue:
    stat = None
    value = None
    unit = None

    def __init__(self, stat: str, value: str, unit: str = None):
        self.stat = stat
        self.value = value
        self.unit = unit


class ActionType(Enum):
    IMMEDIATE = 1
    SWIFT = 2
    MOVE = 3
    STANDARD = 4
    FULL_ROUND = 5

    def __str__(self):
        return "-".join(self.name.split('_')).title()


class CastingDuration(Enum):
    INSTANTANEOUS = 1
    CONCENTRATION = 2
    ROUNDS = 3
    DESCRIPTION = 4

    def __str__(self):
        return self.name.title()

class Labelled:
    name: str

    def __init__(self, name: str, sub_type: str):
        self.sub_type = sub_type
        self.name = name

    def label_type(self):
        return re.sub(r'Card$', '', self.__class__.__name__).lower()

class Action(Labelled):
    action_type: ActionType

    def __init__(self, name: str, action_type: ActionType, sub_type: str, description: List[str],
                 stat_blocks: List[StatWithValue]):
        Labelled.__init__(self, name, sub_type)
        self.action_type = action_type
        self.sub_type = sub_type
        self.description = description
        self.stat_blocks = stat_blocks


class Attack(Action):
    def __init__(self, name: str, action_type: ActionType, sub_type: str, description: List[str],
                 stat_blocks: List[StatWithValue]):
        super().__init__(name, action_type, sub_type, description, stat_blocks)


class Spell(Action):
    def __init__(self, name: str, action_type: ActionType, sub_type: str, description: List[str],
                 stat_blocks: List[StatWithValue], spell_duration: CastingDuration):
        super().__init__(name, action_type, sub_type, description, stat_blocks)
        self.spell_duration = spell_duration


class Card(Labelled):
    name: str
    sub_type: str
    flavour: str = None
    description: List[str] = []
    grants_actions: List[Action]
    stat_blocks: List[StatWithValue] = []
    special_quote: str = None

    def __init__(self, name: str, sub_type: str, flavour: str, description: List[str], grants_actions: List[Action],
                 stat_blocks: List[StatWithValue], **kwargs):
        Labelled.__init__(self, name, sub_type)
        self.flavour = flavour
        self.description = description
        self.grants_actions = grants_actions
        self.stat_blocks = stat_blocks
        self.special_quote = kwargs.get("special_quote", None)
        self.full_image = kwargs.get("full_image", None)


"""
class ActionCard(Action, Card):
    def __init__(self, name: str, sub_type: str, flavour: str, description: List[str], grants_actions: List[Action],
                 stat_blocks: List[StatWithValue], action_type: ActionType):
        Card.__init__(self, name, sub_type, flavour, description, grants_actions, stat_blocks)
        Action.__init__(self, name, action_type, sub_type, description, stat_blocks)
"""


class ClassCard(Card):
    def __init__(self, name: str, sub_type: str, flavour: str, description: List[str], grants_actions: List[Action],
                 stat_blocks: List[StatWithValue], **kwargs):
        super().__init__(name, sub_type, flavour, description, grants_actions, stat_blocks, **kwargs)


class AttackCard(Attack, Card):
    def __init__(self, name: str, sub_type: str, flavour: str, description: List[str], grants_actions: List[Action],
                 stat_blocks: List[StatWithValue], action_type: ActionType):
        Attack.__init__(self, name, action_type, sub_type, description, stat_blocks)
        Card.__init__(self, name, sub_type, flavour, description, grants_actions, stat_blocks)


class DefenceCard(Card):
    def __init__(self, name: str, sub_type: str, flavour: str, description: List[str], grants_actions: List[Action],
                 stat_blocks: List[StatWithValue], **kwargs):
        super().__init__(name, sub_type, flavour, description, grants_actions, stat_blocks, **kwargs)


class SpellCard(Spell, Card):
    def __init__(self, name: str, sub_type: str, flavour: str, description: List[str], grants_actions: List[Action],
                 stat_blocks: List[StatWithValue], action_type: ActionType, spell_duration: CastingDuration):
        Card.__init__(self, name, sub_type, flavour, description, grants_actions, stat_blocks)
        Spell.__init__(self, name, action_type, sub_type, description, stat_blocks, spell_duration)


class CantripCard(SpellCard):
    def __init__(self, name: str, sub_type: str, flavour: str, description: List[str], grants_actions: List[Action],
                 stat_blocks: List[StatWithValue], action_type: ActionType, spell_duration: CastingDuration):
        super().__init__(name, sub_type, flavour, description, grants_actions, stat_blocks, action_type, spell_duration)


class AbilityCard(Card):
    def __init__(self, name: str, sub_type: str, flavour: str, description: List[str], grants_actions: List[Action],
                 stat_blocks: List[StatWithValue], **kwargs):
        super().__init__(name, sub_type, flavour, description, grants_actions, stat_blocks, **kwargs)


class WeaponCard(Card):
    ammo_type: str

    def __init__(self, name: str, sub_type: str, flavour: str, description: List[str], grants_actions: List[Action],
                 stat_blocks: List[StatWithValue], ammo_type: str = None):
        super().__init__(name, sub_type, flavour, description, grants_actions, stat_blocks)
        self.ammo_type = ammo_type


class AmmunitionCard(Card):
    def __init__(self, name: str, sub_type: str, flavour: str, description: List[str], grants_actions: List[Action],
                 stat_blocks: List[StatWithValue]):
        super().__init__(name, sub_type, flavour, description, grants_actions, stat_blocks)


martial_prowess = ClassCard(
    "Martial Prowess",
    "class",
    "Your skill in combat in unparallelled amongst your peers",
    [
        "Search your deck for 2 Ability cards of type: Feat and add them to your hand."
    ],
    [],
    []
)

spontaneous_healing = ClassCard(
    "Spontaneous Healing",
    "class",
    "Your proclivity for healing others manifests in your spellcasting",
    [
        "Discard a Spell card from your hand. If you do not have any Spell cards in your hand, you cannot play this card. Search your deck for any Spell card whose name begins Cure Wounds and play it."
    ],
    [],
    []
)

basic_attack = AttackCard(
    "Basic Attack",
    "melee",
    None,
    [
        "On your turn, you may make a single melee attack"
    ],
    [],
    [
        StatWithValue("To-hit", "+1"),
        StatWithValue("Damage", "1d3", "NL")
    ],
    ActionType.STANDARD
)

heavy_wooden_shield = DefenceCard(
    "Shield, Heavy Wooden",
    "shield",
    None,
    [
        "When this card is in play, gain a +1 bonus to AC"
    ], [],
    [
        StatWithValue("AC", "+1")
    ]
)
chain_shirt = DefenceCard(
    "Chain Shirt",
    "armour",
    None,
    [],
    [],
    [
        StatWithValue("AC", "+4")
    ]
)

sturdy_shield = WeaponCard(
    "Sturdy Shield",
    "buckler",
    None,
    [
        "Attach this card to an in-play Defence card with the Shield type. Once this card is in play, gain the following action:"
    ], [
        Attack(
            "Shield Bash",
            ActionType.STANDARD,
            "melee",
            [],
            [
                StatWithValue("To-hit", "+0"),
                StatWithValue("Damage", "1d4", "B")
            ]
        )
    ],
    []
)

greataxe = WeaponCard(
    "Greataxe",
    "two-handed",
    "This enormous, double-headed axe looks like it takes substantial strength to even lift, let alone swing",
                      [], [],
    [
        StatWithValue("To-hit", "+1"),
        StatWithValue("Damage", "1d12+1", "S")
    ]
)

blowgun = WeaponCard(
    "Blowgun",
    "two-handed",
    None,
    [],
    [],
    [
        StatWithValue("Range", "40ft/60ft/80ft/90ft"),
        StatWithValue("To-hit", "0/-1/-2/-3"),
        StatWithValue("Damage", "1d2", "P")
    ],
    "dart"
)

feathered_dart = AmmunitionCard(
    "Feathered Dart",
    "dart",
    None,
    [],
    [],
    [
        StatWithValue("Damage", "+2", "P"),
        StatWithValue("Uses", "□ □ □ □ □ □ □ □ □ □")
    ]
)

sunder = AttackCard(
    "Sunder",
    "combat manoeuvre",
    None,
    [
    "Make a Combat Manoeuvre check against an enemy in Reach. If successful, select one in-play Weapon card of any type, or one in-play Defence card of type Armour or Shield belonging to that enemy and discard it",
    "While this card is in play, if you are the subject of a Sunder attack, use the CMD granted by this card"
],
    [],
    [
        StatWithValue("CMB", "+1"),
        StatWithValue("CMD", "11")
    ],
    ActionType.STANDARD
)

opportune_combatant = AbilityCard(
    "Opportune Combatant",
    "feat",
    None,
    [
        "If an enemy passes through a square within your Reach, you may take the Attack of Opportunity Action. Each time you do this, one Use of this card is consumed"
    ],[
        Attack(
            "Attack of Opportunity",
            ActionType.IMMEDIATE,
            "melee",
            [
                "Make an Attack with an Action cost of Standard or less granted by in-play cards (other than this one)"
            ],
            []
        )
    ],
    [
        StatWithValue("Uses", "□ □ □ □ □ □ □ □")
    ]
)

double_swing = AttackCard(
    "Double Swing",
    "melee",
    None,
    [
        "You may take two Actions of cost Standard or lower provided by any in-play card. Where these actions have Stat Blocks that match this card's, this card's Stat Blocks replace them."
    ],
    [],
    [
        StatWithValue("To-hit", "+2/+0")
    ],
    ActionType.FULL_ROUND
)

two_weapon_fighting = AttackCard(
    "Two-Weapon Fighting",
    "melee",
    None,
    [
        "You may attach up to two Weapon cards of type One-Handed to this card",
        "You make an attack with each hand. The two attacks use the following To-hit values as a base (add weapon modifiers as usual). You may use the attached Weapon cards in any order"
    ],
    [],
    [
        StatWithValue("To-hit", "+2/+0")
    ],
    ActionType.FULL_ROUND
)

disarm = AttackCard("Disarm", "combat manoeuvre", None, [
    "Make a Combat Manoeuvre check against an enemy. If successful, return the Weapon card to the player's hand",
    "While this card is in play, if you are the subject of a Disarm attack, use the CMD granted by this card"], [], [
                        StatWithValue("CMB", "+1"),
                        StatWithValue("CMD", "11")
                    ], ActionType.STANDARD)

power_attack = AbilityCard("Power Attack", "feat", None, [
    "Return an in-play Defence card to your hand. If you have no Defence cards in play, you cannot play this card. When you take your Action, any Attack you make is subject to the following Stat modifications:"],
                           [], [
                               StatWithValue("To-hit", "-1"),
                               StatWithValue("Damage", "+2")
                           ])

combat_expertise = AbilityCard(
    "Combat Expertise",
    "feat",
    None,
    [
        "You may attach a Defence card from your hand to this card. You may ignore the usual maximum of one Defence card of each type. On each turn, before you take an Action, you must decide whether or not the attached Defence card counts as in-play for this turn. If the attached Defence card is in-play, any Attack actions are subject to the following Stat modifications:"
    ],
    [],
    [
        StatWithValue("To-hit", "-1")
    ]
)

acid_splash = CantripCard(
    "Acid Splash",
    "conjuration",
    "You hurl a few flecks of acid at an enemy",
    [
        "Make a Ranged Touch attack with the following Stats:"
    ],
    [],
    [
        StatWithValue("To-hit", "+0"),
        StatWithValue("Damage", "1d3", "Acid"),
        StatWithValue("Range", "25", "FT")
    ],
    ActionType.STANDARD,
    CastingDuration.INSTANTANEOUS
)

bonus_arcane_power = AbilityCard(
    "Bonus Arcane Power",
    "class feature",
    None,
    [
        "If this card has no Spell cards attached to it, you may attach a Spell of type Evocation with a cast time of Standard or lower from your hand",
        "If this card has a Spell card attached to it, gain the following Action:"
    ],
    [
        Spell(
            "Arcane Specialism: Evocation",
            ActionType.STANDARD,
            "evocation",
            [
                "Cast the Spell attached to this card. When you discard the Spell, also discard this card"
            ],
            [],
            CastingDuration.DESCRIPTION
        )
    ],
    []
)

bonded_object = AttackCard(
    "Bonded Object",
    "spellcast",
    None,
    [
        "You may select any Spell in play or in your hand with a cast time of Standard or lower. Cast that Spell, then return the card to your hand. Afterwards, discard this card"
    ],
    [],
    [],
    ActionType.STANDARD
)

shield_spell = SpellCard(
    "Shield",
    "abjuration",
    "You summon a shimmering disc of force between you and your enemies",
    [
        "Gain a bonus to your AC.",
        "Additionally, while this Spell is active, if you are the target of a Spell with Magic Missile in its name, that Spell automatically misses"
    ],
    [],
    [
        StatWithValue("AC", "+4"),
        StatWithValue("Duration", "10", "rounds")
    ],
    ActionType.STANDARD,
    CastingDuration.ROUNDS
)

defensive_training = DefenceCard(
    "Defensive Training",
    "racial",
    "Raised amongst the Gnomes, you have had many intensive lessons on how to avoid trouble from the bigger folk",
    [
        "If you are the subject of an Attack by a creature of type Giant, you gain a bonus to your AC"
    ],
    [],
    [
        StatWithValue("AC", "+4")
    ],
    special_quote="They may be big, but they're slower and much stupider than you"
)

reckless_warrior = ClassCard(
    "Reckless Warrior",
    "class",
    None,
    [
        "Search your deck for one Defence card and one Weapon card. Discard the Defence card. You may immediately attach the Weapon card to an appropriate in-play Attack or add it to your hand"
    ],
    [],
    []
)

prepared_spellcaster = ClassCard(
    "Prepared Spellcaster",
    "class",
    None,
    [
        "Search your deck for two Spell cards. Discard one and place the other into your hand"
    ],
    [],
    []
)

spontaneous_spellcaster = ClassCard(
    "Spontaneous Spellcaster",
    "class",
    None,
    [
        "Search your discard pile for one Spell card and place it into your hand"
    ],
    [],
    []
)

force_missile = AbilityCard(
    "Force Missile",
    "spell-like",
    None,
    [
        "When you play this card, search your deck for a Spell with the name Magic Missile and attach it to this card. On your turn, as a Standard Action, you may cast the attached Spell without discarding it. Doing so consumes one Use of this card.",
        "Once this card's Uses are expended, or if at the end of your turn there is no Spell card attached to this card, discard this card and all attached Spell cards"
    ],
    [
        Spell(
            "Magic Missile",
            ActionType.STANDARD,
            "evocation",
            [
                "The effects and Stats of this Spell are per the attached Spell card with the name Magic Missile"
            ],
            [],
            CastingDuration.INSTANTANEOUS
        )
    ],
    [],
    full_image=True
)

channel_positive_energy = AbilityCard(
    "Channel Positive Energy",
    "supernatural",
    None,
    [
        "Each time one of these Actions is taken, one Use of this card is consumed"
    ],
    [
        Action(
            "Channel Positive Energy",
            ActionType.STANDARD,
            "supernatural",
            [
                "You infuse living creatures in the area with positive energy, restoring their health"
            ],
            [
                StatWithValue("Radius", "30", "ft"),
                StatWithValue("Health recovered", "3d8")
            ]
        ),
        Action(
            "Channel Positive Energy",
            ActionType.STANDARD,
            "supernatural",
            [
                "You blast undead creatures in the area with positive energy, depleting their unlife"
            ],
            [
                StatWithValue("Radius", "30", "ft"),
                StatWithValue("Damage", "3d8")
            ]
        ),
    ],
    [
        StatWithValue("Uses", "□ □ □ □ □ □ □ □")
    ],
    full_image=True
)

magic_missile_1 = SpellCard(
    "Magic Missile",
    "evocation",
    "A missile of magical energy emerges from your fingertips and seeks its target unerringly",
    [],
    [],
    [
        StatWithValue("Target", "2", "creatures"),
        StatWithValue("Range", "100", "ft"),
        StatWithValue("Damage", "1d4+1", "Force")
    ],
    ActionType.STANDARD,
    CastingDuration.INSTANTANEOUS
)

flare = CantripCard(
    "Flare",
    "evocation",
    None,
    [
        "You cause a burst of light to appear in front of a single target creature. If that creature is sighted, it gains the Dazzled condition"
    ],
    [],
    [
        StatWithValue("Range", "25", "ft"),
        StatWithValue("Save", "DC11", "Fort"),
        StatWithValue("Duration", "10", "rounds")
    ],
    ActionType.STANDARD,
    CastingDuration.ROUNDS
)

mage_hand = CantripCard(
    "Mage Hand",
    "transmutation",
    None,
    [
        "You point your finger at a distant object and move it around at will. You may propel it up to 15ft per round in any direction"
    ],
    [],
    [
        StatWithValue("Range", "25", "ft")
    ],
    ActionType.STANDARD,
    CastingDuration.CONCENTRATION
)

improved_initiative_ability = AbilityCard(
    "Improved Initiative",
    "feat",
    "Your reactions are quicker than most",
    [
        "At the start of an encounter, you may draw one extra card"
    ],
    [],
    [
        StatWithValue("Draw", "+1")
    ]
)

improved_initiative_class = ClassCard(
    "Improved Initiative",
    "class",
    "Your reactions are quicker than most",
    [
        "Draw 2 cards"
    ],
    [],
    [
        StatWithValue("Draw", "+1")
    ]
)
