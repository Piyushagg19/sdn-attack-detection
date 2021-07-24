from loghandler import Logger

import requests
import random
import time
from datetime import datetime
import os
import csv

# api end point
HOST = 'http://localhost'
PORT = ':8080'

# attack dataset file
CSV_FILE = 'attack_logs.csv'
log = Logger().getlogger(__name__)


def main():
    # run the loop every 10 second
    while True:

        # fetching list of switches
        resp = requests.get(HOST + PORT + '/stats/switches').json()

        if len(resp) > 0:
            # randomly selecting a switch, an in_port & an out_port
            dpid = random.choice(resp)
            in_port = random.choice([1, 2, 3, 4])
            out_port = random.choice([1, 2, 3, 4])

            # json format flow data
            data = {
                'dpid': dpid,
                'priority': 32768,
                'idle_timeout': 30,
                'hard_timeout': 30,
                'match': {
                    'in_port': in_port
                },
                'actions': [
                    {
                        'type': 'OUTPUT',
                        'port': out_port
                    }
                ]
            }

            # making post request to add new flow entry in switch
            log.info('post data : ' + str(data))
            resp = requests.post(HOST + PORT + '/stats/flowentry/add', json=data)
            log.info('resp : ' + str(resp))

            # preparing data to write to file
            curr_timestamp = datetime.utcnow().strftime('%s')
            fields = {'time': curr_timestamp, 'datapath': data['dpid'], 'in-port': in_port,
                      'action': data['actions'], 'out-port': out_port}

            # checking if file already exist
            flag = os.path.isfile(CSV_FILE)

            with open(CSV_FILE, 'a') as f:
                header = list(fields.keys())
                writer = csv.DictWriter(f, fieldnames=header)

                # writing header if file is being created for first time
                if not flag:
                    writer.writeheader()

                writer.writerow(fields)
        time.sleep(30)


main()
