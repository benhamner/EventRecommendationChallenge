from dateutil.parser import parse
import pandas as pd
import os

def get_paths():
    """
    Redefine data_path and submissions_path here to run the benchmarks on your machine
    """
    data_path = os.path.join(os.environ["DataPath"], "EventRecommendation", "Release1")
    submission_path = os.path.join(os.environ["DataPath"], "EventRecommendation", "Submissions")
    return data_path, submission_path

def get_user_events_dict(df):
    user_events_dict = {user: [] for user in df["user"]}

    for i, row in df.iterrows():
        user_events_dict[row["user"]].append(row["event"])    

    return user_events_dict

def get_train_test_df(data_path = None):
    if data_path is None:
        data_path, submission_path = get_paths()

    train = pd.read_csv(os.path.join(data_path, "train.csv"),
        converters={"timestamp": parse})
    test = pd.read_csv(os.path.join(data_path, "test.csv"),
        converters={"timestamp": parse})
    return train, test

def get_event_attendees(data_path = None):
    if data_path is None:
        data_path, submission_path = get_paths()

    event_attendees_path = os.path.join(data_path, "event_attendees.csv")
    event_attendees = pd.read_csv(event_attendees_path)
    return event_attendees

def write_submission(submission_name, user_events_dict, submission_path=None):
    if submission_path is None:
        data_path, submission_path = get_paths()

    users = sorted(user_events_dict)
    events = [user_events_dict[u] for u in users]

    submission = pd.DataFrame({"User": users, "Events": events})
    submission[["User", "Events"]].to_csv(os.path.join(submission_path, submission_name), index=False)

def get_event_responses_dict(events, responded_users):
    def parse_users(u):
        if type(u) == str:
            return [int(x) for x in u.split(" ")]
        return [u]

    return {e: parse_users(u) for e, u in zip(events, responded_users)}
