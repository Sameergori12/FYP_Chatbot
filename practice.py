'''import shutil

change = '/change Chicken Pakodi-0'

edit = change[8:].strip()
if edit == 'default':
    shutil.copyfile('original_menuitems.txt', 'temp_menuitems.txt')
    print("Item Prices have set to their default values")
    print(edit)
else:
    fan, nan = edit.replace(':', ':').replace('-', ':').split(':')

    a = {}
    with open("original_menuitems.txt") as f:
        for line in f:
            (k, v) = line.replace(':', ':').replace('-', ':').split(':')
            a[k] = float(v)

    a[fan] = nan

    if '0' in a.values():
        print('This is not original menu list')
        print(a.values())

    with open("temp_menuitems.txt", 'w') as f:
        for key, value in a.items():
            f.write('%s: %.2f\n' % (key, float(value)))
'''

'''from geopy.geocoders import Nominatim
import time
from pprint import pprint

# instantiate a new Nominatim client
app = Nominatim(user_agent="tutorial")

# get location raw data
location = app.geocode("Ashok Colony,Kapra, India").raw
# print raw data
pprint(location)'''

from geopy.geocoders import Nominatim
from geopy import distance

geolocator = Nominatim(user_agent='geoapiExercises')

input_place1 = 'Ashok Colony, Telangana'
input_place2 = 'Gismat Arabic Restaurant Jubilee Hills, Jubilee Hills, Hyderabad, Telangana 500033'

place1 = geolocator.geocode(input_place1)
place2 = geolocator.geocode(input_place2)

print(place1)
print(place2)

Lat1, Long1 = 17.4299296940903, 78.41130927055349
Lat2, Long2 = (17.490421), (78.561083)

location1 = (Lat1, Long1)
location2 = (Lat2, Long2)
dist = distance.distance(location1, location2).km
print(dist, ' Kms')
location = geolocator.reverse(Lat1, Long1)
print('address: ', location.address)
if(dist<10):
    print("Yes sir")
elif (dist>10):
    print('Distance beyond range')