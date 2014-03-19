import time

import logging
import twitter

logger = logging.getLogger(__name__)

class Printer:
    def print(self, text):
        raise NotImplementedError()

class Lifemachine:
    def __init__(self, query, printer, oauth_token, oauth_secret, consumer_key, consumer_secret,
                 wait_between_queries=15, wait_between_prints=30, count=5):
        self.query = query
        self.connection = twitter.Twitter(auth=twitter.OAuth(
            oauth_token, oauth_secret, consumer_key, consumer_secret
            ))
        logger.info('Lifemachine, engage!')
        self.wait_between_queries = 15
        self.wait_between_prints = 30
        self.count = 5
        self.since_id = None
        self.printer = printer

    def run(self):
        while True:
            logger.debug('Iteration with since_id={}'.format(self.since_id))
            self.do_iteration()
            logger.debug('Iteration done, waiting {} seconds...'.format(
                self.wait_between_queries))
            time.sleep(self.wait_between_queries)

    def do_iteration(self):
        """
        Search for a specific number of tweets, maintain `self.since_id`,
        call `print_tweet` accordingly.
        """
        kw = {'q': self.query, 'count': self.count}
        # First iteration?
        if self.since_id is not None:
            kw['since_id'] = self.since_id
        tweets = self.connection.search.tweets(**kw)
        last_id = self.since_id or 0
        for status in tweets['statuses']:
            last_id = max(last_id, status['id'])
            # reject retweets
            if 'retweeted_status' in status:
                continue
            self.print_tweet(status)
            time.sleep(self.wait_between_prints)
        self.since_id = last_id

    def print_tweet(self, status):
        """
        *status* is a Tweet object.
        """
        username = status['user']['screen_name']
        text = status['text']
        output = '@{}: {}'.format(username, text)
        logger.info('Printing tweet: {}'.format(output))
        self.print_text(output)

    def print_text(self, text):
        """
        *text* is a string.
        """
        self.printer.print(text)
