import configparser
import os.path
import os
import argparse

class Cats:
    def __init__(self, name, breed, color, age):
        self.name = name
        self.breed = breed
        self.color = color
        self.age = age

    def __str__(self):
        return f"{self.name} ({self.breed}, {self.color}, {self.age})"

    def __eq__(self, other):
        if isinstance(other, Cats):
            return (self.breed == other.breed and
                    self.color == other.color and
                    self.age == other.age)
        return NotImplemented


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', nargs = '?', default='settings\settings.ini', help="Name of the settings file")
args = parser.parse_args()
print(args.file)

if os.path.isfile(args.file):
    config = configparser.ConfigParser()
    config.read(args.file, encoding="UTF-8")

    daisy_arr = config['CATS']['DAISY'].split(', ')
    sima_arr = config['CATS']['SIMA'].split(', ')
    milen_arr = config['CATS']['MILEN'].split(', ')

    Daisy = Cats(daisy_arr[0], daisy_arr[1], daisy_arr[2],  int(daisy_arr[3]))
    Sima = Cats(sima_arr[0], sima_arr[1], sima_arr[2],  int(sima_arr[3]))
    Milen = Cats(milen_arr[0], milen_arr[1], milen_arr[2],  int(milen_arr[3]))

    f = open('instances.txt', 'w')
    f.write(str(Daisy))
    f.write('\n')
    f.write(str(Sima))
    f.write('\n')
    f.write(str(Milen))
    f.close

else:
    print('File not found')