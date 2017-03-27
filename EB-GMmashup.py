import requests
import json

Gmaps_key = "AIzaSyB-sNsbt0EbgVnl7P41NSasVJUaOUMgYTI"
Ebrite_key = "ROZPHY2OWBELU4MKCZKA"

# Return coordinates from Google API for current location
def get_coordinates(address):
	response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}'.format(address))
	address_dict = response.json()
	lat = (address_dict['results'][0]['geometry']['location']['lat'])
	lng = (address_dict['results'][0]['geometry']['location']['lng'])
	coord = [lat, lng]
	return coord

# Return 10 nearby events based on coordinates
def get_events(coordinates):
	lat = coordinates[0]
	lng = coordinates[1]

	# Call Eventbrite API search function with coordinates as parameters
	event_list = requests.get(
    	"https://www.eventbriteapi.com/v3/events/search/?location.latitude={0}&location.longitude={1}".format(lat, lng),
    	headers = {
        	"Authorization": "Bearer ROZPHY2OWBELU4MKCZKA"
    	},
    	verify = True,  # Verify SSL certificate
	)
	event_dict = event_list.json()

	# Retrieve events and package into dictionary with event, id, and date
	events = {}
	for i in range(0, 10):
		curr_event = event_dict['events'][i]['name']['text']
		curr_id = event_dict['events'][i]['id']

		# List and format event date for readability
		curr_date_orig= event_dict['events'][i]['start']['local']
		curr_date_day = curr_date_orig[0:10]
		curr_date_time = curr_date_orig[11:16]
		curr_date = "at " + curr_date_time + " on " + curr_date_day

		# event -> id -> date
		events[curr_event] = {}
		events[curr_event][curr_id] = curr_date

	return events

# Print events in formatted way
def print_events(events):
	count = 0
	for event, ids in events.items():
		for current, date in ids.items():
			count = count + 1
			print ("%s) " % count) +  event
			print "     " + date
			print ""

# Bring functions together and prompt user for location
def main():
	location = str (raw_input("Type name of location in format: 123 Street, City, ST : \n"))
	coordinates = get_coordinates(location)
	events = get_events(coordinates)
	print_events(events)
	print "Go forth and enjoy new experiences!"


main()
