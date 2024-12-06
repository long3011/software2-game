from geopy import distance
from airport import *
import requests

class Player:
    def __init__(self, name, difficulty, money, airport_list, airport_travelled=None, fuel=1000, hints=3, co2=0):
        if airport_travelled is None:
            airport_travelled = {}
        self.airport_travelled = airport_travelled
        self.name = name
        self.position = start_position
        self.difficulty = difficulty
        self.money = money
        self.airport_list = airport_list
        self.fuel = fuel
        self.hints = hints
        self.co2=co2
    def get_airport_distance(self,location1):  # getting distance between two point, with latitude and longitude as location1, and location 2
        first_airport = self.position.airport_position()
        second_airport = location1
        return distance.distance(first_airport, second_airport).kilometers
    def use_hint(self):  # find the nearest airport
        if self.hints>0:
            compare_list = {}
            for i in self.airport_list:
                end_airport = self.airport_list[i].airport_position()
                compare_list[i] = self.get_airport_distance(end_airport)
            nearest_airport = min(compare_list, key=compare_list.get)
            return nearest_airport, self.airport_list[nearest_airport]
    def fly(self,new_pos_id):
        distance_travel = self.get_airport_distance(self.airport_list[new_pos_id].airport_position())
        self.position = self.airport_list[new_pos_id]
        self.fuel-= round(distance_travel*3.5/100, 1)
        self.co2+= round(distance_travel/10, 1)
        self.airport_travelled[new_pos_id]=self.position
        if new_pos_id in self.airport_list:
            del self.airport_list[new_pos_id]
        return round(distance_travel,2)
    def buy_hints(self):
        if self.money >= 200:
            self.money -= 200
            self.hints += 1
    def buy_fuel(self): #buying fuel
        if self.money >= 500:
            self.money -= 500
            self.fuel += 200
    def show_balance(self):
        return self.money
    def information(self): #convert all object information into string and list to save to a file
        airport_left = {}
        airport_travelled = {}
        for i in self.airport_list:
            airport_left[i]=self.airport_list[i].airport_info()
        for i in self.airport_travelled:
            airport_travelled[i]=self.airport_travelled[i].airport_info()
        return [self.name, self.difficulty, self.money, airport_left,airport_travelled, round(self.fuel,1), self.hints, round(self.co2,1)] #using round because computer sometime become quirky and output weird decimals
    def leaderboard(self):
        total_airport = []
        for i in self.airport_list:
            total_airport.append(self.airport_list[i].airport_ident())
        for i in self.airport_travelled:
            total_airport.append(self.airport_travelled[i].airport_ident())
        total_airport=','.join(total_airport)
        return self.name,total_airport, self.calculate_points()
    def calculate_points(self):  # points calculation
        points=0
        for i in self.airport_travelled:
            points+=self.airport_travelled[i].airport_point()
        return round(((10000 * self.difficulty * points) / ((self.co2 + self.money * 5) / 2)), 2)
    def remaining_airports(self):
        return len(self.airport_list)
    def fuel_left(self):
        return self.fuel
