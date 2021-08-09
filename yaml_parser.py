import codecs
import pprint

from yaml import safe_load

from cards import Card, ActionCost, AbilityRequirement, Action, StatWithValue, Image, CastingDuration

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

def parse_action(raw_action: dict) -> Action:
    return Action(
        raw_action['name'],
        raw_action['type'],
        raw_action['sub-type'],
        ActionCost(**raw_action['action-cost']),
        raw_action.get('description', []),
        [parse_stat_with_value(swv) for swv in raw_action.get('stat-blocks', [])],
        next(cd for cd in CastingDuration if cd.name == raw_action.get('casting-duration').upper()) if 'casting-duration' in raw_action else None
    )

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
    feature_image = Image(raw_card['feature-image'].get('type'),
                          raw_card['feature-image'].get('data')) if 'feature-image' in raw_card else Image()
    full_image = Image(raw_card['full-image'].get('type'),
                       raw_card['full-image'].get('data')) if 'full-image' in raw_card else None
    return Card(name,
        card_type,
        card_sub_type,
        ability_requirement,
        level_requirement,
        flavour,
        description,
        [parse_action(raw_action) for raw_action in raw_card.get('granted-actions', [])],
        stat_blocks,
        action_cost=action_cost,
        casting_time=next(cd for cd in CastingDuration if cd.name == raw_card.get('casting-duration').upper()) if 'casting-duration' in raw_card else None,
        feature_image=feature_image,
        full_image=full_image,
        special_quote=special_quote
    )

if __name__ == '__main__':
    [pprint.pprint(raw_card) for raw_card in load_cards("example_card.yaml")]
