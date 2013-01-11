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

def main():
    data_path = os.path.join(os.environ["DataPath"], "EventRecommendation")
    release_path = os.path.join(data_path, "Release1")

    user_interest_path = os.path.join(data_path, "RawData4", "events_shown.csv")

    user_interest = pd.read_csv(user_interest_path, converters={"timestamp": parse})
    user_interest = user_interest.sort("timestamp")

    users = set(user_interest["user"])
    user_events_dict = get_user_events_dict(user_interest)

    print("Number of Users: %d" % len(users))
    print("Number of Users With Interested Events: %d" % len([x for x in users if sum(user_interest["interested"][user_interest["user"]==x])>0]))
    print("Number of Users With Not Interested Events: %d" % len([x for x in users if sum(user_interest["not_interested"][user_interest["user"]==x])>0]))
    print("Min Number of Events Shown: %d" % min(len(user_events_dict[user]) for user in user_events_dict))
    print("Max Number of Events Shown: %d" % max(len(user_events_dict[user]) for user in user_events_dict))

if __name__=="__main__":
    main()