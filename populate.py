# create a database  called pollution-db2 mysql

from sqlalchemy import create_engine
import pandas
from sqlalchemy_utils import database_exists, create_database

try:

    # Create a connection to the database
    engine = create_engine('mysql+pymysql://root:@localhost/pollution-db2')

    # Create the database if it doesn't exist
    if not database_exists(engine.url):
        create_database(engine.url)

    dbcon = engine.connect()

    df = pandas.read_csv('clean.csv', sep=';')

    data = [
        [188, "AURN Bristol Centre", '51.4572041156, -2.58564914143'],
        [203, 'Brislington Depot', '51.4417471802, -2.55995583224'],
        [206, 'Rupert Street', '51.4554331987, -2.59626237324'],
        [209, 'IKEA M32', '51.4752847609, -2.56207998299'],
        [213, 'Old Market', '51.4560189999, -2.58348949026'],
        [215, 'Parson Street School', '51.432675707, -2.60495665673'],
        [228, 'Temple Meads Station', '51.4488837041, -2.58447776241'],
        [270, 'Wells Road', '51.4278638883, -2.56374153315'],
        [271, 'Trailer Portway P&R', '51.4899934596, -2.68877856929'],
        [375, 'Newfoundland Road Police Station', '51.4606738207, -2.58225341824'],
        [395, "Shiner's Garage", '51.4577930324, -2.56271419977'],
        [452, 'AURN St Pauls', '51.4628294172, -2.58454081635'],
        [447, 'Bath Road', '51.4425372726, -2.57137536073'],
        [459, 'Cheltenham Road \ Station Road', '51.4689385901, -2.5927241667'],
        [463, 'Fishponds Road', '51.4780449714, -2.53523027459'],
        [481, 'CREATE Centre Roof', '51.447213417, -2.62247405516'],
        [500, 'Temple Way', '51.4579497129, -2.58398909033'],
        [501, 'Colston Avenue', '51.4552693825, -2.59664882861'],
        [672, 'Marlborough Street', '51.4552693825, -2.59664882861']
    ]

    station = pandas.DataFrame(data, columns=['id', 'name', 'geo_point_2d'])
    # insert station into the database using pandas
    station.to_sql('station', con=dbcon, if_exists='replace', index=False, index_label='id')

    # Read the clean.csv file
    reading = pandas.read_csv('clean.csv', sep=';')
    # Remove the SiteID , Locatiion ,geo_point_2d columns
    reading = reading.drop(['Location', 'geo_point_2d'], axis=1)
    # Rename the SiteID column to station_id
    reading = reading.rename(columns={'SiteID': 'station_id'})

    # Insert the data into the database using pandas
    reading.to_sql('reading', con=dbcon, if_exists='replace', index=True, index_label='id')

    # Read the schema csv file
    schema = pandas.read_csv('schema.csv', sep=',')
    schema.to_sql('schema', con=dbcon, if_exists='replace', index=True, index_label='id')

    # close database connection
    dbcon.close()

except Exception as e:
    print(e)
    print('Error: An error occurred whiles running script.')
