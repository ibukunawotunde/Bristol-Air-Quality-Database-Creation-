from sqlalchemy import create_engine
import pandas


engine = create_engine('mysql+pymysql://root:@localhost/pollution-db2')
dbcon = engine.connect()

# Read the first  100 records from the reading table
df = pandas.read_sql_query('select * from reading limit 100', dbcon)


file_sql = open('insert-100.sql', 'w')
# Loop through the data frame and generate inset statements using column names
for index, row in df.iterrows():

    #Start from next line
    file_sql.write('\r\n')
    line = f"""INSERT INTO `pollution-db2`.reading ( `Date Time`, NOx, NO2, `NO`, PM10, NVPM10, VPM10, `NVPM2.5`, `PM2.5`, `VPM2.5`, CO, O3, SO2, Temperature, RH, `Air Pressure`, DateStart, DateEnd, `Current`, `Instrument Type`)
 values ('{row['Date Time'] or ''}', {row['NOx'] or 0}, {row['NO2'] or 0}, {row['NO'] or 0}, {row['PM10'] or 0}, {row['NVPM10'] or 0}, {row['VPM10'] or 0}, {row['NVPM2.5'] or 0}, {row['PM2.5'] or 0}, {row['VPM2.5'] or 0}, {row['CO'] or 0}, {row['O3'] or 0}, {row['SO2'] or 0}, {row['Temperature'] or 0}, {row['RH'] or 0}, {row['Air Pressure'] or 0}, '{row['DateStart']}', '{row['DateEnd']}', {row['Current']}, '{row['Instrument Type']}');"""
    # Replace None values with NULL
    file_sql.write(line)


file_sql.close()

# Close the connection
dbcon.close()