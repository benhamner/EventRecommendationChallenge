import random
import util as u 
import pandas as pd

def main():
    train, test = u.get_train_test_df()
    user_events_dict = u.get_user_events_dict(test)
    event_attendees = u.get_event_attendees()
    event_yes = u.get_event_responses_dict(event_attendees["event"], event_attendees["yes"])

    for user in user_events_dict:
        user_events_dict[user] = sorted(user_events_dict[user],
            key=lambda e: len(event_yes[e]), reverse=True)

    u.write_submission("event_popularity_benchmark.csv", user_events_dict)

if __name__=="__main__":
    main()