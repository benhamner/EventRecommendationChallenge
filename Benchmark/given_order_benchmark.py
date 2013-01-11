import random
import util as u 

def main():
    train, test = u.get_train_test_df()
    user_events_dict = u.get_user_events_dict(test)
    u.write_submission("given_order.csv", user_events_dict)

if __name__=="__main__":
    main()