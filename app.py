import argparse
import mysql.connector
import configparser
import json

#config.ini parser
config = configparser.ConfigParser()
config.read('./config.ini')

# replace password with actual password, can now run queries and see results!
cnx = mysql.connector.connect(user=config['MYSQL']['USER'], password=config['MYSQL']['PASSWORD'], host=config['MYSQL']['HOST'], port=config['MYSQL']['PORT'], database=config['MYSQL']['DATABASE'])
query_content = cnx.cursor()

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

    query = "show databases;"

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

            # because of how the president_county_candidate CSV is, determining winner should be through
            # whoever has biggest number of counties won in a state (first past the post)
            # WIP query
            query = f"""SELECT DISTINCT candidate FROM president_county_candidate WHERE
                        state = '{input_state_full}' and
                        COUNT(won) =  MAX(COUNT(won)) FROM (SELECT COUNT(won) FROM president_county_candidate WHERE
                            state = '{input_state_full}'
                        )
                    """
            print("Loser in this state of " + input_state_full + " is " + placeholder)
        elif (input_action == "winner"):
            placeholder = "not trump lol"
            print("Determining: " + input_action)
            print("Winner in this state of " + input_state_full + " is " + placeholder)
        elif (input_action == "tweets"):
            # we can try to move the overhead of this into the actual arg parser so it'll be easier to sanitize
            print("Tweet selection:")
            print("Please choose what you want to know")
            
        query_content.execute(query)

        results = query_content.fetchall()

        for result in results:
            print(result)


    # cnx.close()
