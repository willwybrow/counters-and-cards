import codecs
import re
import cards
from typing import List, Union

from prettierfier import prettify_html

from bs4 import Tag, BeautifulSoup, NavigableString

modifier_re = re.compile(r'([+-]\d+)')
dice_re = re.compile(r'(\d+)d(\d+)([+-]\d+)')

def get_all_cards():
    return sorted([getattr(cards, name) for name in dir(cards) if isinstance(getattr(cards, name), cards.Card)], key=lambda c: c.label_type())

def generate(cards_to_generate: List[cards.Card]) -> BeautifulSoup:
    soup = BeautifulSoup()
    html = Tag(name="html")
    soup.append(html)
    head = Tag(name="head")
    html.append(head)
    title = Tag(name="title")
    head.append(title)
    title_string = NavigableString("Card Folio")
    title.append(title_string)
    link = Tag(name="link", attrs={'rel': 'stylesheet', 'type': 'text/css', 'href': 'cards.css'})
    head.append(link)

    body = Tag(name="body")
    html.append(body)

    for card in cards_to_generate:
        body.append(generate_card(card))

    """
    body.append(generate_card(cards.martial_prowess))
    body.append(generate_card(cards.spontaneous_healing))
    body.append(generate_card(cards.basic_attack))
    body.append(generate_card(cards.heavy_wooden_shield))
    body.append(generate_card(cards.chain_shirt))
    body.append(generate_card(cards.sturdy_shield))
    body.append(generate_card(cards.greataxe))
    body.append(generate_card(cards.blowgun))
    body.append(generate_card(cards.feathered_dart))
    body.append(generate_card(cards.sunder))
    body.append(generate_card(cards.opportune_combatant))
    body.append(generate_card(cards.double_swing))
    body.append(generate_card(cards.two_weapon_fighting))
    body.append(generate_card(cards.disarm))
    body.append(generate_card(cards.power_attack))
    body.append(generate_card(cards.combat_expertise))
    body.append(generate_card(cards.acid_splash))
    body.append(generate_card(cards.bonus_arcane_power))
    body.append(generate_card(cards.bonded_object))
    body.append(generate_card(cards.shield_spell))
    body.append(generate_card(cards.defensive_training))
    body.append(generate_card(cards.reckless_warrior))
    body.append(generate_card(cards.prepared_spellcaster))
    body.append(generate_card(cards.spontaneous_spellcaster))
    body.append(generate_card(cards.force_missile))
    body.append(generate_card(cards.channel_positive_energy))
    body.append(generate_card(cards.magic_missile_1))
    body.append(generate_card(cards.flare))
    body.append(generate_card(cards.mage_hand))
    body.append(generate_card(cards.improved_initiative_ability))
    body.append(generate_card(cards.improved_initiative_class))
    """

    return soup


def generate_header(headable_thing: Union[cards.Card, cards.Action]) -> Tag:
    header = Tag(name="header", attrs={'data-type': headable_thing.label_type()})
    h1 = Tag(name="h1")
    h1.append(NavigableString(headable_thing.name))
    header.append(h1)
    if hasattr(headable_thing, 'action_type'):
        aside = Tag(name="aside", attrs={'class': 'action-type'})
        aside.append(NavigableString(headable_thing.action_type.__str__()))
        header.append(aside)
    if hasattr(headable_thing, 'spell_duration'):
        aside = Tag(name="aside", attrs={'class': 'spell-duration'})
        aside.append(NavigableString(headable_thing.spell_duration.__str__()))
        header.append(aside)
    return header


def generate_card_figure(card: cards.Card) -> Tag:
    figure = generate_sub_figure(card)
    if card.full_image is not None:
        pass
    elif card.feature_image is not None:
        figure.insert(0, Tag(name="img", attrs={
            'src': "data:image/{};base64, {}".format(card.feature_image.mime_type, card.feature_image.base64_data)
        }))
    return figure


def generate_sub_figure(typed_thing: Union[cards.Action, cards.Card]) -> Tag:
    figure = Tag(name="figure")
    figcaption = Tag(name="figcaption")
    h2 = Tag(name="h2", attrs={'class': 'type'})
    h2.append(NavigableString(typed_thing.sub_type.title()))
    figcaption.append(h2)
    figure.append(figcaption)
    return figure


def generate_stats_with_values(stats_with_values: List[cards.StatWithValue]) -> Tag:
    for stat_with_value in stats_with_values:
        swv_section = Tag(name="section")
        swv_section['class'] = "stat-with-value"
        swv_stat = Tag(name="label")
        swv_section.append(swv_stat)
        swv_stat.append(NavigableString(stat_with_value.stat))
        swv_value = Tag(name="data")
        swv_section.append(swv_value)
        swv_value['value'] = stat_with_value.value
        swv_value.append(NavigableString(stat_with_value.value))
        if stat_with_value.unit is not None:
            small = Tag(name="small")
            swv_value.append(small)
            small.append(NavigableString(stat_with_value.unit))
        yield swv_section

def generate_description_line(description_line: str) -> Tag:
    p_description = Tag(name="p")
    for text_segment in modifier_re.split(description_line):
        if modifier_re.match(text_segment) is not None:
            strong_modifier = Tag(name="strong")
            p_description.append(strong_modifier)
            strong_modifier.append(NavigableString(text_segment))
        else:
            p_description_string = NavigableString(description_line)
            p_description.append(p_description_string)
    return p_description

def generate_footer(card: cards.Card) -> Tag:
    footer = Tag(name="footer")
    h3 = Tag(name="h3", attrs={'class': 'level-requirement'})
    h3.append(NavigableString(str(card.level_requirement)))
    footer.append(h3)
    if isinstance(card, cards.WeaponCard) and card.ammo_type is not None:
        aside = Tag(name="aside", attrs={"class": "ammunition"})
        aside.append(NavigableString(card.ammo_type))
        footer.append(aside)
    return footer

def generate_card(card: cards.Card):
    article = Tag(name="article", attrs={'class': 'playing-card', 'data-ability-requirement': str(card.ability_requirement)})
    if card.full_image is not None:
        article['style'] = 'background-blend-mode: exclusion; background-image: url("data:image/{};base64,{}"); background-size: cover; background;'.format(card.full_image.mime_type, card.full_image.base64_data)
    header = generate_header(card)
    article.append(header)
    article.append(generate_card_figure(card))

    section = Tag(name="section")
    if card.special_quote is not None:
        blockquote = Tag(name="blockquote")
        blockquote.append(NavigableString(card.special_quote))
        section.append(blockquote)
    if card.flavour is not None:
        p_flavour = Tag(name="p")
        section.append(p_flavour)
        p_flavour['class'] = "flavour"
        p_flavour_string = NavigableString(card.flavour)
        p_flavour.append(p_flavour_string)
    [section.append(generate_description_line(description_line)) for description_line in card.description]
    [section.append(swv_section) for swv_section in generate_stats_with_values(card.stat_blocks)]
    article.append(section)
    for granted_action in card.grants_actions:
        action_section = Tag(name="section")
        article.append(generate_header(granted_action))
        article.append(generate_sub_figure(granted_action))
        [action_section.append(generate_description_line(description_line)) for description_line in granted_action.description]
        [action_section.append(swv_section) for swv_section in generate_stats_with_values(granted_action.stat_blocks)]
        article.append(action_section)
    article.append(generate_footer(card))
    return article

def generate_card_folio(cards_to_generate: List[cards.Card]):
    soup = generate(cards_to_generate)

    print(soup.prettify())

    with codecs.open("card_folio.html", mode="w") as file:
        file.write(prettify_html(soup.prettify()))

    print("Done")

if __name__ == "__main__":
    generate_card_folio(get_all_cards())
