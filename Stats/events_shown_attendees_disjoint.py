from __future__ import division
from copy import copy
import csv
from dateutil.parser import parse
import numpy  as np
import os
import pandas as pd
import random

class CsvDialect(csv.Dialect):
    def __init__(self):
        self.delimiter = ','
        self.doublequote = True
        self.escapechar = None
        self.lineterminator = "\n"
        self.quotechar = '"'
        self.quoting = csv.QUOTE_MINIMAL
        self.skipinitialspace = False
        self.strict = False

def get_user_events_dict(df):
    user_events_dict = {user: [] for user in df["user"]}

    for i, row in df.iterrows():
        user_events_dict[row["user"]].append(row["event"])    

    return user_events_dict

def get_event_responses_dict(events, responded_users):
    def parse_users(u):
        if type(u) == str:
            return [int(x) for x in u.split(" ")]
        return [u]

    return {e: parse_users(u) for e, u in zip(events, responded_users)}

def main():
    data_path = os.path.join(os.environ["DataPath"], "EventRecommendation")
    release_path = os.path.join(data_path, "Release1")

    user_interest_path = os.path.join(data_path, "RawData4", "events_shown.csv")
    event_attendees_path = os.path.join(release_path, "event_attendees.csv")

    user_interest = pd.read_csv(user_interest_path, converters={"timestamp": parse})
    user_interest = user_interest.sort("timestamp")

    event_attendees = pd.read_csv(event_attendees_path)

    event_yes = get_event_responses_dict(event_attendees["event"], event_attendees["yes"])
    event_maybe = get_event_responses_dict(event_attendees["event"], event_attendees["maybe"])
    event_invited = get_event_responses_dict(event_attendees["event"], event_attendees["invited"])
    event_no = get_event_responses_dict(event_attendees["event"], event_attendees["no"])

    users = set(user_interest["user"])
    user_events_dict = get_user_events_dict(user_interest)

    for user in user_events_dict:
        for event in user_events_dict[user]:
            try:
                if user in event_yes[event]:
                    print("User %d in Event Yes %d" % (user, event))
                if user in event_maybe[event]:
                    print("User %d in Event Maybe %d" % (user, event))
                if user in event_no[event]:
                    print("User %d in Event No %d" % (user, event))
                if user in event_invited[event]:
                    print("User %d in Event Invited %d" % (user, event))
            except KeyError:
                print(event)

if __name__=="__main__":
    main()
