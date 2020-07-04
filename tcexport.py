#
# tcexport.py --
#   Convert TinyCards decks from a Duolingo "Drive-Thru portal" export file
#   into a flat CSV file suitable for import into Anki or another flashcard app
#
# author: Michael Portuesi
# date: 2020-06-28
#
import argparse
from exporter import Exporter

# main conversion / processing loop
def process(input_file_name, output_file_name):
    exporter = Exporter()

    try:
        decks = exporter.read_and_convert_decks(input_file_name)
    except Exception:
        print ("Error while reading CSV file:")
        raise

    try:
        exporter.output_decks(decks, output_file_name)
    except Exception:
        print ("Error while writing CSV file:")
        raise

    return len(decks)

def main():
    ap = argparse.ArgumentParser(
    description ='tcexport version '+ Exporter.VERSION + \
    ' -- Convert TinyCards decks from a Duolingo "Drive-Thru portal" export file ' \
    'into a flat CSV file suitable for import into Anki or another flashcard app',
    epilog='The output CSV file will contain the cards from all TinyCards decks. Each ' \
    'output CSV record has three fields: front, back, and tag. The name of the TinyCards ' \
    'deck is converted into a tag, and attached to all cards of that deck.')
    ap.add_argument("-i", "--infile", required=True, help="input file name (in duolingo CSV format)")
    ap.add_argument("-o", "--outfile", required=True, help="output file name (CSV export)")
    args=vars(ap.parse_args())

    try:
        Exporter().verify_input_file(args["infile"])
        deck_count = process(args["infile"], args["outfile"])
        print(f'Processed {deck_count} decks from {args["infile"]}.')
    except Exception as ex:
        print(ex)

main()
