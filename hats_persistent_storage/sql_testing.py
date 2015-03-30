from sys import argv
import mysqlinterface as sqlinter
from structures import Device, Room, House, User

# Read in mysql arguments.
script, usr, pwd, dtbs = argv;

# Initialize the interface and reset the table.
sql = sqlinter.MySQLInterface(usr, pwd, dtbs)
sql.reset_tables()

# Initialize devices and lists of devices.
dev1 = Device("home1", "1", "1", "cat1", "1")
dev2 = Device("home1", "2", "2", "cat2", "1")
dev3 = Device("home1", "3", "1", "dog1", "2")
dev4 = Device("home1", "4", "2", "dog2", "2")
dev5 = Device("home1", "5", "1", "monkey1")
dev6 = Device("home1", "6", "2", "monkey2")
r1devs = [dev1, dev2]
r2devs = [dev3, dev4]
hdevs = [dev5, dev6]

# Initialize rooms and lists of rooms
room1 = Room("home1", "1", "cat room", r1devs)
room2 = Room("home1", "2", "dog room", r2devs)
hrooms = [room1, room2]

# Initialize house
house1 = House("home1", "pet home", hrooms, hdevs)
house2 = House("home2", "people home", None, None)

# Insert it all recursively.
sql.insert_house(house1)
sql.insert_house(house2)

# Insert users.
user1 = User("1", "OBAMA")
user2 = User("2", "OSAMA")
sql.insert_user(user1)
sql.insert_user(user2)

print "\nHouse Devices:"
for dev in sql.get_house_devices("home1", None):
  print dev._data

print "\nRoom1 Devices:"
for dev in sql.get_room_devices("home1", "1", None):
  print dev._data

print "\nHouse Devices Type 1"
for dev in sql.get_house_devices("home1", "1"):
  print dev._data

print "\nRoom1 Devices Type 2"
for dev in sql.get_room_devices("home1", "1", "2"):
  print dev._data

print "\nRoom3 Devices (No prints - Room3 doesn't exist)"
for dev in sql.get_room_devices("home1", "3"):
  print dev._data

print "\nUser Datas"
print sql.get_user_data("1")
print sql.get_user_data("2")

print "\nHouse Datas"
print sql.get_house_data("home1")
print sql.get_house_data("home2")
print sql.get_house_data("home3") # should return none

print "\nRoom Datas"
print sql.get_room_data("home1", "1")
print sql.get_room_data("home1", "2")
print sql.get_room_data("home1", "3") # should return none

print "\nDevice Datas"
print sql.get_device_data("home1", "1", "1")
print sql.get_device_data("home1", "2", "1")
print sql.get_device_data("home1", "3", "2")
print sql.get_device_data("home1", "4", "2")
print sql.get_device_data("home1", "5")
print sql.get_device_data("home1", "6")
print sql.get_device_data("home1", "1", "3") # should return none
print sql.get_device_data("home1", "7") # should return none

print "\nModifying user1 Data"
sql.update_user("1", "Mr. President")
print sql.get_user_data("1")

print "\nModifying home1 Data"
sql.update_house("home1", "ANIMALS EVERYWHERE")
print sql.get_house_data("home1")

print "\nModifying room1 data"
sql.update_room("home1", "1", "HELLO KITTY HOUSE")
print sql.get_room_data("home1", "1")

print "\nModifying device4 data"
sql.update_device("home1", "4", "Lassie", "2")
print sql.get_device_data("home1", "4", "2")

print "\nModifying device5 data"
sql.update_device("home1", "5", "Curious George")
print sql.get_device_data("home1", "5")

print "\nRemoving device4, printing device4 info and devices in room2"
sql.delete_device("home1", "4", "2")
print sql.get_device_data("home1", "4", "2")
for dev in sql.get_room_devices("home1", "2"):
  print dev._data

print "\nRemoving Room1, printing room1 info and devices in home1"
sql.delete_room("home1", "1")
print sql.get_room_data("home1", "1")
for dev in sql.get_house_devices("home1"):
  print dev._data

print "\nRemoving Home1, printing home info and devices in home1"
sql.delete_house("home1")
print sql.get_house_data("home1")
for dev in sql.get_house_devices("home1"):
  print dev._data

print "\nRemoving user1, printing user1 info"
sql.delete_user("1")
print sql.get_user_data("1")