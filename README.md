# tinycards-exporter

## Description
Convert TinyCards decks from a Duolingo "Drive-Thru portal" export file
into a flat CSV file suitable for import into Anki or another flashcard app.

For more information about the TinyCards shutdown and how to export your data,
see the [announcement on the TinyCards website](https://support.duolingo.com/hc/en-us/articles/360043909772-Tinycards-Announcement).

## Requirements
The script was developed using Python 3.8.3 but will probably work with any version of Python 3.  It's not rocket science.

## Command Line Arguments
```
-h, --help  show help message and exit
-i, --infile INFILE  input file name
-o, --outfile OUTFILE  output file name (CSV export)
```
The input file is in TinyCards CSV format, this is the 'decks.csv' file in the Drive-Thru portal download.

The output CSV file will contain the cards from all TinyCards decks. Each output CSV record has three fields: front,
back, and tag.

The name of each TinyCards deck is converted into a tag, and attached to all cards of that deck.

## Limitations
 - If your deck in TinyCards has additional fields for each card face, they are not retained.  Only the first line of each card is transferred.
 - Decks with pictures are not supported.
