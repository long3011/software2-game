import mysql.connector

connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sql_password',
            database='flight_game',
            collation='utf8mb4_general_ci',
            autocommit=True
        )

class Airport:
    def __init__(self,ident, name,type, lat,lon,country_name,country_continent,point=100):  # rename continent names in airport list for easier reading
        self.ident = ident
        self.name = name
        self.type = type
        self.lat = lat
        self.lon = lon
        self.country_name = country_name
        self.country_continent = country_continent
        if self.country_continent == 'EU':
            self.country_continent = 'Europe'
        elif self.country_continent == 'NA':
            self.country_continent = 'North America'
        elif self.country_continent == 'SA':
            self.country_continent = 'South America'
        elif self.country_continent == 'AF':
            self.country_continent = 'Africa'
        elif self.country_continent == 'AN':
            self.country_continent = 'Antarctica'
        elif self.country_continent == 'AS':
            self.country_continent = 'Asia'
        elif self.country_continent == 'OC':
            self.country_continent = 'Oceania/Australia'
        else:
            pass
        self.point=point
    def airport_ident(self): #return ICAO code of airport
        return self.ident
    def airport_name(self): #return name of airport
        return self.name
    def airport_type(self): #return type of airport
        return self.type
    def airport_position(self): #return position of airport in lat and lon
        return self.lat,self.lon
    def airport_country(self): #return the country where the airport is in
        return self.country_name,self.country_continent
    def airport_point(self):
        return self.point
    def airport_info(self):
        return [self.ident,self.name,self.type,self.lat,self.lon,self.country_name,self.country_continent,self.point]
def airports(amount): #getting airports information from sql and creating the airport dictionary
    airport_list = {}
    cursor = connection.cursor()
    sql = (
        f"SELECT airport.ident, airport.NAME, airport.type, airport.latitude_deg, airport.longitude_deg, country.name,airport.continent "
        f"FROM country, airport "
        f"WHERE airport.iso_country = country.iso_country "
        f"having TYPE = 'medium_airport' OR TYPE = 'large_airport' "
        f"ORDER BY RAND() LIMIT {amount};")
    cursor.execute(sql)
    output = cursor.fetchall()
    for i in range(len(output)):
        airport_list[str(i+1)] = Airport(output[i][0],output[i][1], output[i][2], output[i][3], output[i][4], output[i][5], output[i][6])
    return airport_list
start_position = Airport('EFHK', 'Helsinki Vantaa Airport', 'large_airport', 60.3172, 24.963301, 'FI', 'Finland', 'EU')