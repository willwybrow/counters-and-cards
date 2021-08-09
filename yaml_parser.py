import codecs
import pprint

from yaml import safe_load

from cards import Card, AttackCard, ActionCost, AbilityRequirement, Action, StatWithValue, Attack, Spell, \
    CastingDuration, AbilityCard, AmmunitionCard, CantripCard, ClassCard, DefenceCard, SpellCard, WeaponCard, Image, \
    ActionCard

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def load_cards(filename):
    with codecs.open(filename, mode="r") as yaml_file:
        for raw_card in safe_load(yaml_file)['cards']:
            yield parse_card(raw_card)


def parse_stat_with_value(raw_swv: dict) -> StatWithValue:
    return StatWithValue(str(raw_swv['name']), str(raw_swv['value']), str(raw_swv['unit']) if raw_swv.get('unit') is not None else None)


def parse_card(raw_card: dict) -> Card:
    action_cost = ActionCost(**raw_card['action-cost']) if 'action-cost' in raw_card else None
    ability_requirement = AbilityRequirement.ANY if raw_card.get('requirements', {}).get('ability') == 'any' else next(
        ar for ar in AbilityRequirement if ar.name == "{}_{}".format(raw_card.get('requirements', {}).get('advantage'),
                                                                     raw_card.get('requirements', {}).get(
                                                                         'ability')).upper())
    level_requirement = raw_card.get('requirements', {}).get('level')
    name = raw_card['name']
    card_type = raw_card['type']
    card_sub_type = raw_card['sub-type']
    flavour = raw_card.get('flavour', None)
    special_quote = raw_card.get('quote', None)
    description = raw_card.get('description', [])
    stat_blocks = [parse_stat_with_value(swv) for swv in raw_card.get('stat-blocks', [])]
    granted_actions = []
    feature_image = Image(raw_card['feature-image'].get('type'),
                          raw_card['feature-image'].get('data')) if 'feature-image' in raw_card else Image()
    full_image = Image(raw_card['full-image'].get('type'),
                       raw_card['full-image'].get('data')) if 'full-image' in raw_card else None
    for raw_granted_action in raw_card.get('granted-actions', []):
        if raw_granted_action['type'] == 'action':
            granted_actions.append(
                Action(
                    raw_granted_action['name'],
                    ActionCost(**raw_granted_action['action-cost']),
                    raw_granted_action['sub-type'],
                    raw_granted_action['description'],
                    [parse_stat_with_value(swv) for swv in raw_granted_action.get('stat-blocks', [])]
                )
            )
        elif raw_granted_action['type'] == 'attack':
            granted_actions.append(
                Attack(
                    raw_granted_action['name'],
                    ActionCost(**raw_granted_action['action-cost']),
                    raw_granted_action['sub-type'],
                    raw_granted_action['description'],
                    [parse_stat_with_value(swv) for swv in raw_granted_action.get('stat-blocks', [])]
                )
            )
        elif raw_granted_action['type'] == 'spell':
            granted_actions.append(
                Spell(
                    raw_granted_action['name'],
                    ActionCost(**raw_granted_action['action-cost']),
                    raw_granted_action['sub-type'],
                    raw_granted_action['description'],
                    [parse_stat_with_value(swv) for swv in raw_granted_action.get('stat-blocks', [])],
                    next(cd for cd in CastingDuration if cd.name == raw_granted_action.get('casting-duration').upper())
                )
            )
    if card_type is None:
        raise TypeError("Card must have a type")
    elif card_type == 'ability':
        return AbilityCard(
            ability_requirement,
            name,
            card_sub_type,
            flavour,
            description,
            granted_actions,
            stat_blocks,
            feature_image=feature_image,
            full_image=full_image,
            special_quote=special_quote,
            level_requirement=level_requirement
        )
    elif card_type == 'action':
        return ActionCard(
            ability_requirement,
            name,
            card_sub_type,
            flavour,
            description,
            granted_actions,
            stat_blocks,
            action_cost,
            feature_image=feature_image,
            full_image=full_image,
            special_quote=special_quote,
            level_requirement=level_requirement
        )
    elif card_type == 'ammunition':
        return AmmunitionCard(
            ability_requirement,
            name,
            card_sub_type,
            flavour,
            description,
            granted_actions,
            stat_blocks,
            feature_image=feature_image,
            full_image=full_image,
            special_quote=special_quote,
            level_requirement=level_requirement
        )
    elif card_type == 'attack':
        return AttackCard(
            ability_requirement,
            name,
            card_sub_type,
            flavour,
            description,
            granted_actions,
            stat_blocks,
            action_cost,
            feature_image=feature_image,
            full_image=full_image,
            special_quote=special_quote,
            level_requirement=level_requirement
        )
    elif card_type == 'cantrip':
        return CantripCard(
            ability_requirement,
            name,
            card_sub_type,
            flavour,
            description,
            granted_actions,
            stat_blocks,
            action_cost,
            next(cd for cd in CastingDuration if cd.name == raw_card.get('casting-duration').upper()),
            feature_image=feature_image,
            full_image=full_image,
            special_quote=special_quote,
            level_requirement=level_requirement
        )
    elif card_type == 'class':
        return ClassCard(
            ability_requirement,
            name,
            card_sub_type,
            flavour,
            description,
            granted_actions,
            stat_blocks,
            feature_image=feature_image,
            full_image=full_image,
            special_quote=special_quote,
            level_requirement=level_requirement
        )
    elif card_type == 'defence':
        return DefenceCard(
            ability_requirement,
            name,
            card_sub_type,
            flavour,
            description,
            granted_actions,
            stat_blocks,
            feature_image=feature_image,
            full_image=full_image,
            special_quote=special_quote,
            level_requirement=level_requirement
        )
    elif card_type == 'spell':
        return SpellCard(
            ability_requirement,
            name,
            card_sub_type,
            flavour,
            description,
            granted_actions,
            stat_blocks,
            action_cost,
            next(cd for cd in CastingDuration if cd.name == raw_card.get('casting-duration').upper()),
            feature_image=feature_image,
            full_image=full_image,
            special_quote=special_quote,
            level_requirement=level_requirement
        )
    elif card_type == 'weapon':
        return WeaponCard(
            ability_requirement,
            name,
            card_sub_type,
            flavour,
            description,
            granted_actions,
            stat_blocks,
            feature_image=feature_image,
            full_image=full_image,
            special_quote=special_quote,
            level_requirement=level_requirement
        )
    else:
        raise TypeError("Card type {} not recognised".format(card_type))


if __name__ == '__main__':
    [pprint.pprint(raw_card) for raw_card in load_cards("example_card.yaml")]
