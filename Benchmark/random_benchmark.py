import random
import util as u 

def main():
    train, test = u.get_train_test_df()
    user_events_dict = u.get_user_events_dict(test)

    for user in sorted(user_events_dict):
        random.shuffle(user_events_dict[user])

    u.write_submission("random.csv", user_events_dict)

if __name__=="__main__":
    main()