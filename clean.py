import pandas as pd

data = {
    188: 'AURN Bristol Centre',
    203: 'Brislington Depot',
    206: 'Rupert Street',
    209: 'IKEA M32',
    213: 'Old Market',
    215: 'Parson Street School',
    228: 'Temple Meads Station',
    270: 'Wells Road',
    271: 'Trailer Portway P&R',
    375: 'Newfoundland Road Police Station',
    395: "Shiner's Garage",
    452: 'AURN St Pauls',
    447: 'Bath Road',
    459: 'Cheltenham Road \ Station Road',
    463: 'Fishponds Road',
    481: 'CREATE Centre Roof',
    500: 'Temple Way',
    501: 'Colston Avenue',
    672: 'Marlborough Street'
}

station = pd.DataFrame(list(data.items()), columns=['SiteID', 'Location'])
reading = pd.read_csv('crop.csv', sep=';')

# Create a new df with the SiteID and Location columns where SiteID and Location  match what is in the reading df
check = reading.SiteID.isin(station.SiteID) & reading.Location.isin(station.Location)

# Mismatch records
mismatch = reading[~check][['SiteID', 'Location']]

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(mismatch)

clean_df = reading[check]

# Save the file into clean.csv
clean_df.to_csv('clean.csv', index=False, sep=';')