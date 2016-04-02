import requests
import geopy
import time
from geopy.geocoders import Nominatim

URL = 'https://api.hailoapp.com'


class Hailo:
	def __init__(self, token):
		self.token = token

	def auth(self):
		return requests.get(URL + '/status/up', headers={'Authorization': "token " + self.token})

	def near(self, longitude, latitude):
		response = requests.get(URL + '/drivers/near?latitude={0}&longitude={1}'.format(latitude, longitude), headers={'Authorization': "token " + self.token})
		return response.json()

	def near_location(self, location):
		geolocator = Nominatim()
		location = geolocator.geocode(location)
		return self.near(location.longitude, location.latitude)

	def tracking(self, interval, location='', longitude=0, latitude=0):
		''' Record stat by tracking of available drivers by location
		'''
		drivers = self._get_near_drivers(location, longitude, latitude)
		while True:
			time.sleep(interval)
			new_drivers = self._get_near_drivers(location, longitude, latitude)
			for i in range(0, len(drivers)):
				pass

	def _get_near_drivers(self, location, longitude, latitude):
		drivers = []
		if location is not '':
			drivers = self.near_location(location)
		if longitude is not 0 and latitude is not 0:
			drivers = self.near(longitude, latitude)

		if drivers is None:
			return Exception("Unexpected error")
			
		if 'drivers' not in drivers:
			raise Exception("'drivers' field not in response")
		return drivers['drivers']
