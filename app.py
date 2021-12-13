import argparse
import mysql.connector
import json

# cnx = mysql.connector(user="a5hua", password="password", host="", database="marmoset04.shoshin.uwaterloo.ca")

# argument parsing structure. this is where will define inputs for user and modify whether they're positional, optional, typed, etc
parser = argparse.ArgumentParser(description="US 2020 Elections Application")
parser.add_argument('state', default="CA")
parser.add_argument('action', default="winner")

args = parser.parse_args()

# where the magic happens. the main that runs everything
if __name__ == "__main__":
    input_state = args.state.upper()
    input_action = args.action.lower()

    # print(args.state)
    # print(args.action)

    # we want to ensure that whatever state we inputted is a valid one (we ask users to input abbrev for sake of brevity)
    with open('./US_states.json') as f:
        state_name_data = json.load(f)

        if input_state not in state_name_data:
            raise Exception("Sorry, incorrect state abbreviation.")

        input_state_full = state_name_data[input_state]
        print("Selected state: " + state_name_data[input_state])
        # print("Determining: " + input_action)

        # python in this current version probably doesn't have switch case still, so we will use if/else instead
        # within each action, we will custom build a query to the MYSQL server
        if (input_action == "loser"):
            placeholder = "trump lol"
            print("Determining: " + input_action)
            print("Loser in this state of " + input_state_full + " is " + placeholder)
        elif (input_action == "winner"):
            placeholder = "not trump lol"
            print("Determining: " + input_action)
            print("Winner in this state of " + input_state_full + " is " + placeholder)
        elif (input_action == "tweets"):
            # we can try to move the overhead of this into the actual arg parser so it'll be easier to sanitize
            print("Tweet selection:")
            print("Please choose what you want to know")
            

    # cnx.close()
