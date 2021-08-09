
import glob
import itertools
from html_generator import generate_card_folio
from yaml_parser import load_cards

if __name__ == "__main__":
    generate_card_folio(itertools.chain(*[load_cards(file) for file in glob.glob("cards/*.yaml")]))

