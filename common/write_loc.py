#import unicodecsv as csv
import csv

# These columns may vary depending on what pops you have added to the game
# Change as necessary
id_column = 0
name_column = 10

generated_localisation = open("GENERATED_LOCALISATION.yml","w",encoding="latin-1")

setup_csv = open("province_setup.csv", "r",encoding="latin-1")
reader = csv.reader(setup_csv, delimiter=";")

def write_loc():
    with generated_localisation as f:
        f.write("l_english:\n")
        for row in reader:
            f.write( " PROV" + row[id_column] + ":0 " + '"' + row[name_column] + '"' + "\n" )


write_loc()
