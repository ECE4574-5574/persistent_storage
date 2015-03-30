import json

def DumpJsonList(listToDump):
  dicts = []
  for item in listToDump:
    dicts.append(item.to_JSON())
  return json.dumps(dicts)

class Device:
  def __init__(self, house_id, device_id, device_type, data, room_id=None):
    self._house_id = house_id
    if (room_id != None):
      self._room_id = room_id
    self._device_id = device_id
    self._device_type = device_type
    self._data = data
  def to_JSON(self):
    jsonDict = {'device-id': self._device_id, 'device-type': self._device_type, 'blob': self._data}
    return jsonDict 

class Room:
  def __init__(self, house_id, room_id, data, devices):
    self._house_id = house_id
    self._room_id = room_id
    self._data = data

    self._devices = []
    if not (devices is None):
      for device in devices:
        self._devices.append(device)


class House:
  def __init__(self, house_id, data, rooms, devices):
    self._house_id = house_id
    self._data = data

    self._rooms = []
    if not (rooms is None):
      for room in rooms:
        self._rooms.append(room)

    self._devices = []
    if not (devices is None):
      for device in devices:
        self._devices.append(device)


class User:
  def __init__(self, user_id, data):
    self._user_id = user_id
    self._data = data