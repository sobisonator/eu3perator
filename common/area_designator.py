import pandas as pd
import unicodedata, unidecode, re

# Input file
SETUP_CSV = "province_setup.csv"
# Output file
f_area = open("areas_output.txt", "w")
f_region = open("regions_output.txt", "w")

# Turn the province_setup CSV into a dataframe
df = pd.read_csv(
    SETUP_CSV,
    sep=';',
    low_memory=False
)

def sanitise_string(input_string):
    output_string = str(input_string).replace(" ", "_").replace(".","_")
    return unidecode.unidecode(output_string)
    #return ''.join(c for c in unicodedata.normalize('NFD', output_string)
    #              if unicodedata.category(c) != 'Mn')

non_area_provinces = open("default.map")
non_area_provinces_data = non_area_provinces.read()
pattern = "RANGE {(.*)}"
non_area_ranges = re.findall(pattern, non_area_provinces_data)
non_area_ranges = [i.split(" ") for i in non_area_ranges]
new_non_area_ranges = []
for x in non_area_ranges:
    x = [i for i in x if i]
    new_non_area_ranges.append(x)
non_area_ranges = new_non_area_ranges

def check_if_area_needed(province_id):
    # Check if the province ID is any of the ranges specified
    try:
        province_id = int(province_id)
    except:
        return False
    for province_range in non_area_ranges:
        if province_id >= int(province_range[0]) and province_id <= int(province_range[1]):
            return False
    if " " + str(province_id) + " " not in non_area_provinces_data:
        return True
    else:
        return False

# Get a list of all areas in your CSV
areas = df.AREA
# Only count provinces that have a tradegood - i.e. land provinces
for n, area in enumerate(areas):
    areas[n] = sanitise_string(area)
    
areas = areas.unique().tolist()


# Function to print to a text file all provinces in an area in the Imperator
# format
def output_area(area, provinces):
    f_area.write(area + " = {\n" +
            "   provinces = {\n")
    provids_list = provinces['PROVID'].tolist()
    for provid in provids_list:
        if check_if_area_needed(provid):
            f_area.write("      " + str(provid) + "\n")
    f_area.write("   }\n}\n\n")

# Get all the provinces in each area
for area in areas:
    print(area)
    provinces = df.loc[df['AREA'] == area]
    # Sanitise the area string
    area = sanitise_string(area)
    print(area)
    output_area(str(area), provinces)
    print("===DONE===")

# Now generate a regions file with every area as a region to avoid errors
for area in areas:
    # Sanitise the area string
    area = sanitise_string(area)
    f_region.write("region_" + str(area) + " = {\n" +
                   "    areas = {\n" +
                   "        " + str(area) + "\n    }\n}\n"
                   )

f_area.close()
f_region.close()
