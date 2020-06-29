#
# tcexport.py --
#   Convert TinyCards decks from a Duolingo "Drive-Thru portal" export file
#   into a flat CSV file suitable for import into Anki or another flashcard app
#
# author: Michael Portuesi
# date: 2020-06-28
#
import csv, string, argparse

# A flashcard has a front, back and a tag.
class FlashCard(object):
    def __init__(self, front, back, tag):
        self.front = front
        self.back = back
        self.tag = tag

    def __repr__(self):
        return "<FlashCard({front}, {back}, {tag})".format(**self.__dict__)

#
# parse the cards in tinycards' markdown-ish format.
# pass in the card text (multi-line string), get back an array of card objects
#
# current implementation grabs only the first line of text for the front and back
# TODO: parse additional lines in both front and back sides of the card, and append into one string
def parse_cards_for_deck(card_text, tag):
    cards = []
    in_card = False
    in_front = False
    in_back = False
    card_front = ""
    card_back = ""
    for line in card_text.splitlines():
        if "### Card" in line:
            in_card = True
        elif in_card and "Front" in line:
            in_front = True
        elif in_front:
            card_front = line.strip("* ")
            in_front = False
        elif in_card and "Back" in line:
            in_back = True
        elif in_back:
            card_back = line.strip("* ")
            card = FlashCard(card_front,card_back,tag)
            cards.append(card)
            # print(f'Front: {card.front} Back: {card.back} Tag: {card.tag}' )
            in_back = False
            in_card = False
    return cards

# create a tag from supplied text
def tagify(text):
    return text.translate(str.maketrans('','',string.punctuation)).lower().replace(" ", "_")

def read_and_convert_decks(input_file_name):
    decks = {}

    with open(input_file_name, encoding="utf8") as input_csv_file:
        csv_reader = csv.reader(input_csv_file,  delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                deck_name = row[0]
                cards = parse_cards_for_deck(row[3], tagify(deck_name))
                decks[deck_name] = cards
            line_count += 1

    return decks

def output_decks(decks, output_file_name):
    with open(output_file_name, encoding="utf8", mode='w') as output_csv_file:
        csv_writer = csv.writer(output_csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        for deck_name, cards in decks.items():
            for card in cards:
                csv_writer.writerow([card.front, card.back, card.tag])

def process(input_file_name, output_file_name):
    try:
        decks = read_and_convert_decks(input_file_name)
    except Exception:
        print ("Error while reading CSV file:")
        raise

    try:
        output_decks(decks, output_file_name)
    except Exception:
        print ("Error while writing CSV file:")
        raise

    return len(decks)

def main():
    ap = argparse.ArgumentParser(
    description ='Convert TinyCards decks from a Duolingo "Drive-Thru portal" export file ' \
    'into a flat CSV file suitable for import into Anki or another flashcard app',
    epilog='The output CSV file will contain the cards from all TinyCards decks. Each ' \
    'output CSV record has three fields: front, back, and tag. The name of the TinyCards ' \
    'deck is converted into a tag, and attached to all cards of that deck.')
    ap.add_argument("-i", "--infile", required=True, help="input file name (in duolingo CSV format)")
    ap.add_argument("-o", "--outfile", required=True, help="output file name (CSV export)")
    args=vars(ap.parse_args())

    try:
        deck_count = process(args["infile"], args["outfile"])
        print(f'Processed {deck_count} decks from {args["infile"]}.')
    except Exception as ex:
        print(ex)

main()
