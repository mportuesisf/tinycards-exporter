import csv, string

# A flashcard has a front, back and a tag.
class FlashCard(object):
    def __init__(self, front, back, tag):
        self.front = front
        self.back = back
        self.tag = tag

    def __repr__(self):
        return "<FlashCard({front}, {back}, {tag})".format(**self.__dict__)


class Exporter(object):
    def __init__(self):
        pass

    #
    # parse the cards in tinycards' markdown-ish format.
    # pass in the card text (multi-line string), get back an array of card objects
    #
    # current implementation grabs only the first line of text for the front and back
    # TODO: parse additional lines in both front and back sides of the card, and append into one string
    def parse_cards_for_deck(self, card_text, tag):
        cards = []
        in_card = False
        in_front = False
        in_back = False
        card_front = ""
        card_back = ""
        for line in card_text.splitlines():
            if "### Card" in line:
                in_card = True
            elif in_card and not in_front and line.strip() == "Front":
                in_front = True
            elif in_front:
                card_front = line.strip("* ")
                in_front = False
            elif in_card and not in_back and line.strip() == "Back":
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
    def tagify(self, text):
        return text.translate(str.maketrans('','',string.punctuation)).lower().replace(" ", "_")

    def read_and_convert_decks(self, input_file_name):
        decks = {}
        with open(input_file_name, encoding="utf8") as input_csv_file:
            csv_reader = csv.reader(input_csv_file,  delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    deck_name = row[0]
                    cards = self.parse_cards_for_deck(row[3], self.tagify(deck_name))
                    decks[deck_name] = cards
                line_count += 1

        return decks

    def output_decks(self, decks, output_file_name):
        with open(output_file_name, encoding="utf8", mode='w') as output_csv_file:
            csv_writer = csv.writer(output_csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            for deck_name, cards in decks.items():
                for card in cards:
                    csv_writer.writerow([card.front, card.back, card.tag])

    # Look at the first line of the CSV file to verify it's a TinyCards deck export
    def verify_input_file(self, input_file_name):
        headers = ["name","description","coverImage","cards","privacy","language","deleted","createdAt","updatedAt"]
        with open(input_file_name, encoding="utf8") as input_csv_file:
            csv_reader = csv.reader(input_csv_file,  delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    idx = 0
                    for header in headers:
                        if header != row[idx]:
                            raise Exception("Input file is not a TinyCards export CSV file.")
                        idx += 1
