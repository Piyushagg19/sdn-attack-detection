import requests
import random
import logging
import time

HOST = 'http://localhost'
PORT = ':8080'

def main():
	while (True):
		resp = requests.get(HOST + PORT + '/stats/switches').json()
		
		if len(resp) > 0:
			dpid = random.choice(resp)
			in_port = random.choice([1, 2, 3, 4, 5, 6])
			out_port = random.choice([1, 2, 3, 4, 5, 6])
			data = {
				'dpid': dpid,
				'priority': 32768,
				'match': {
					'in_port': in_port
				}
			}
			if(random.choice([True, False])):
				data['actions'] = [
					{
						'type': 'OUTPUT',
						'port': out_port
					}
				]
			else:
				data['actions'] = []

			resp = requests.post(HOST + PORT + '/stats/flowentry/add', json=data)
			print('response of adding new flow' + str(resp))
		time.sleep(10)



main()