import csv
import time
import random
from bot_framework import Bot

class ManualCoordinateRaider:
    def __init__(self, coordinates_file, troop_composition):
        self.coordinates = self.load_coordinates(coordinates_file)
        self.troop_composition = troop_composition
        self.running = True
        self.bot = Bot()

    def load_coordinates(self, coordinates_file):
        with open(coordinates_file, mode='r') as file:
            reader = csv.reader(file)
            return [(int(row[0]), int(row[1])) for row in reader]

    def send_attack(self, x, y):
        # Logic to send attack to (x, y)
        self.bot.attack(x, y, self.troop_composition)

    def start_raid(self):
        while self.running:
            for x, y in self.coordinates:
                self.send_attack(x, y)
                time.sleep(random.randint(300, 900))  # Delay between 5-15 minutes

    def stop_raid(self):
        self.running = False

if __name__ == '__main__':
    coordinates_file = 'coordinates.csv'  # Use path to your CSV
    troop_composition = {'archers': 100, 'cavalry': 50}  # Example composition
    raider = ManualCoordinateRaider(coordinates_file, troop_composition)
    raider.start_raid()