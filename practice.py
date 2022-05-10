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
ald = Lat1, Long1
location = geolocator.reverse(ald)
print('address: ', location.address)
if(dist<10):
    print("Yes sir")
elif (dist>10):
    print('Distance beyond range')


'''
import datetime

def time_in_range(current):
    """Returns whether current is in the range [start, end]"""

    start = datetime.time(10, 0, 0)
    end = datetime.time(23, 0, 0)
    return start <= current <= end



current = datetime.datetime.now().time()

print(time_in_range(current))
# True (if you're not a night owl) ;)'''


"""# import module
from datetime import date

# get current date and time
current_datetime = date.today()
print("Current date & time : ", current_datetime)

# convert datetime obj to string
str_current_datetime = str(current_datetime)

# create a file object along with extension
file_name = str_current_datetime+".txt"
file = open(file_name, 'a')
content = "funny"
file.write(content+"\n\n")
print("File created : ", file.name)
file.close()"""
