#!/usr/bin/env python
# usage: `python parse_twitter.py path/to/twitter/output`

import csv
import sys


def parse_tweets(fname):
    with open(fname) as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            yield row


if __name__ == "__main__":
    tweets = parse_tweets(sys.argv[1] + "/tweets.csv")
    for tweet in tweets:
        print tweet["text"]
