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

def get_user_events_interested_dict(df):
    user_events_interested_dict = {user: [] for user in df["user"]}

    for i, row in df.iterrows():
        if row["interested"] != 1:
            continue
        user_events_interested_dict[row["user"]].append(row["event"])    

    return user_events_interested_dict

def get_valid_solution_users_list(user_events_dict):
    solution_users = sorted(user for user in user_events_dict
        if len(user_events_dict[user])>1)
    return solution_users

def get_solution_data(df, set_str):
    user_events_dict = get_user_events_dict(df)
    user_events_interested_dict = get_user_events_interested_dict(df)

    solution_users = get_valid_solution_users_list(user_events_dict)
    solution_data = [(str(u),
        " ".join([str(event) for event in user_events_interested_dict[u]]),
        set_str) for u in solution_users]
    return solution_data

def main():
    data_path = os.path.join(os.environ["DataPath"], "EventRecommendation")
    release_path = os.path.join(data_path, "Release1")

    user_interest_path = os.path.join(data_path, "RawData4", "events_shown.csv")

    user_interest = pd.read_csv(user_interest_path, converters={"timestamp": parse})
    user_interest = user_interest.sort("timestamp")

    users = set(user_interest["user"])
    print("Number of Users: %d" % len(users))
    print("Number of Users With Interested Events: %d" % len([x for x in users if sum(user_interest["interested"][user_interest["user"]==x])>0]))
    print("Number of Users With Not Interested Events: %d" % len([x for x in users if sum(user_interest["not_interested"][user_interest["user"]==x])>0]))

    p60cutoff = int(0.6*len(users))
    p70cutoff = int(0.7*len(users))

    users_list = list(users)
    random.shuffle(users_list)

    train_users_list = sorted(users_list[:p60cutoff])
    train_users_set = set(train_users_list)
    public_leaderboard_users_list = sorted(users_list[:p70cutoff])
    public_leaderboard_users_set = set(public_leaderboard_users_list)
    private_leaderboard_users_list = sorted(users_list[p70cutoff:])
    private_leaderboard_users_set = set(private_leaderboard_users_list)

    train = user_interest.select(lambda i: user_interest.irow(i)["user"] in train_users_set).sort("user")
    public_leaderboard = user_interest.select(lambda i: user_interest.irow(i)["user"] in public_leaderboard_users_set).sort("user")
    private_leaderboard = user_interest.select(lambda i: user_interest.irow(i)["user"] in private_leaderboard_users_set).sort("user")

    public_solution = get_solution_data(public_leaderboard, "PublicTest")
    private_solution = get_solution_data(private_leaderboard, "PrivateTest")
    solution = copy(public_solution)
    solution.extend(private_solution)
    solution = sorted(solution, key = lambda x: int(x[0]))

    writer = csv.writer(open(os.path.join(release_path, "solution.csv"), "w"), dialect=CsvDialect())
    writer.writerow(["User", "Events", "Usage"])
    writer.writerows(solution)

    test = public_leaderboard.append(private_leaderboard, ignore_index=True)[["user","event", "invited","timestamp"]].sort("user")
    test.to_csv(os.path.join(release_path, "test.csv"), index=False)

    train[["user", "event", "invited", "timestamp", "interested", "not_interested"]].to_csv(os.path.join(release_path, "train.csv"), index=False)

if __name__=="__main__":
    main()