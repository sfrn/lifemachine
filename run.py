import os
import logging

import twitter

import lifemachine

from lifeconfig import *

logger = logging.getLogger(__name__)

class MachinePrinter(lifemachine.Printer):
    def __init__(self, path):
        self.path = path
        self.stream = open(path, 'wb')

    def print(self, text):
        encoded = text.replace('\n', '\n\r').encode('cp437', 'replace')
        self.stream.write(encoded)
        self.stream.write(b'\n\r')
        self.stream.flush()

if not os.path.exists(CREDS):
    twitter.oauth_dance('lifemachine', CONSUMER_KEY, CONSUMER_SECRET, CREDS)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    filename='lifemachine.log',
                    filemode='w')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

oauth_token, oauth_secret = twitter.read_token_file(CREDS)

printer = MachinePrinter(DEVICE)
machine = lifemachine.Lifemachine(QUERY, printer, oauth_token,
        oauth_secret, CONSUMER_KEY, CONSUMER_SECRET,
        wait_between_queries=3*60,
        wait_between_prints=90,
        count=10)
machine.print_statistics()
machine.run()
