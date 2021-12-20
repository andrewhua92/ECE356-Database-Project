import argparse
import mysql.connector
import configparser
import json
import datetime

#config.ini parser
config = configparser.ConfigParser()
config.read('./config.ini')

# replace password with actual password, can now run queries and see results!
cnx = mysql.connector.connect(user=config['MYSQL']['USER'], password=config['MYSQL']['PASSWORD'], host=config['MYSQL']['HOST'], port=config['MYSQL']['PORT'], database=config['MYSQL']['DATABASE'])
query_content = cnx.cursor()

# argument parsing structure. this is where will define inputs for user and modify whether they're positional, optional, typed, etc
parser = argparse.ArgumentParser(description="US 2020 Elections Application")
parser.add_argument('action', default="winner", help="Enter the action you would like to use for this application.")
parser.add_argument('-s', '--state', help="Enter the state you would like to know about.")
parser.add_argument('-c','--candidate', help="The candidate that you would like to know about. Please use 'jb' for Joe Biden or 'dt' for Donald Trump.")
parser.add_argument('-g', '--granular', help="Specifies specific property to look up for the 'tweet' action.")
args = parser.parse_args()

# where the magic happens. the main that runs everything
if __name__ == "__main__":
    if args.state:
        input_state = args.state.upper()
    if args.candidate:
        temp = args.candidate.lower()
        if temp == "jb":
            candidate = "Joe Biden"
        else:
            candidate = "Donald Trump"
    input_action = args.action.lower()

    # print(args.state)
    # print(args.action)

    # query = "show databases;"

    # we want to ensure that whatever state we inputted is a valid one (we ask users to input abbrev for sake of brevity)
    with open('./US_states.json') as f:
        state_name_data = json.load(f)

        # print("Determining: " + input_action)

        # python in this current version probably doesn't have switch case still, so we will use if/else instead
        # within each action, we will custom build a query to the MYSQL server
        if (input_action == "loser"):
            if input_state not in state_name_data:
                raise Exception("Sorry, incorrect state abbreviation.")

            input_state_full = state_name_data[input_state]
            print("Selected state: " + state_name_data[input_state])

            print("Determining: " + input_action)

            # because of how the president_county_candidate CSV is, determining winner should be through
            # whoever has biggest number of counties won in a state (first past the post)
            # WIP query
            query = f"""WITH voteCount AS
                            (SELECT candidate, SUM(total_votes) AS votes FROM president_county_candidate WHERE
                                state = '{input_state_full}'
                                GROUP BY candidate
                                ORDER BY SUM(total_votes) DESC)

                        SELECT candidate FROM voteCount WHERE
                            votes = (SELECT MAX(votes) FROM voteCount);
            """

            query_content.execute(query)

            results = query_content.fetchall()

            placeholder = results[0][0]

            if (placeholder == "Joe Biden"):
                placeholder = "Donald Trump"
            else:
                placeholder = "Joe Biden"

            print("Loser in " + input_state_full + " is " + placeholder)
        elif (input_action == "winner"):
            if input_state not in state_name_data:
                raise Exception("Sorry, incorrect state abbreviation.")

            input_state_full = state_name_data[input_state]
            print("Selected state: " + state_name_data[input_state])

            print("Determining: " + input_action)

            query = f"""WITH voteCount AS
                            (SELECT candidate, SUM(total_votes) AS votes FROM president_county_candidate WHERE
                                state = '{input_state_full}'
                                GROUP BY candidate
                                ORDER BY SUM(total_votes) DESC)

                        SELECT candidate FROM voteCount WHERE
                            votes = (SELECT MAX(votes) FROM voteCount);
            """

            query_content.execute(query)

            results = query_content.fetchall()

            # results returns a list of tuples, hence, the double array precision
            placeholder = results[0][0]

            print("Winner in " + input_state_full + " is " + placeholder)
        elif (input_action == "tweets"):
            # we can try to move the overhead of this into the actual arg parser so it'll be easier to sanitize
            print("Determining: " + input_action) 

            if not args.candidate:
                raise Exception("Sorry, no candidate provided for tweet information. Please use -h for more info.")

            if args.granular:
                granular = args.granular

                tableQuery = "joebiden" if candidate == "Joe Biden" else "donaldtrump"

                granular_options = ["likes", "retweets", "followers", "country", "continent", "city", "state"]
                metadata_options = ["likes", "retweets", "followers"]
                location_options = ["country", "continent", "city", "state"]

                if granular in granular_options:
                    if granular in metadata_options:
                        if not args.state: 
                            query = f""" SELECT user_screen_name, {granular}, state, created_at, tweet FROM hashtag_{tableQuery}
                                WHERE {granular} = (SELECT MAX({granular}) FROM hashtag_{tableQuery})
                            """
                            query_content.execute(query)

                            results = query_content.fetchall()

                            # print(results)
                            name, granular_val, state, created_at, tweet = results[0]

                            if not name or not granular_val or not created_at or not tweet:
                                raise Exception("Sorry, an error occurred and it failed to grab the metadata.")

                            if not state:
                                state = "USA"

                            reword = ""
                            if granular == "followers":
                                reword = " from user"

                            print("The tweet about " + candidate + reword + " with the most " + granular + " of a count of " + str(granular_val) + " is: ")
                            print("\"" + tweet + "\"")
                            print("The tweet was made by " + name + ", posted in " + state + " at " + created_at.strftime("%c"))
                        else:

                            if input_state not in state_name_data:
                                raise Exception("Sorry, incorrect state abbreviation.")

                            input_state_full = state_name_data[input_state]
                            print("Selected state: " + state_name_data[input_state])

                            query = f"""WITH stateTweetData AS
                                            (SELECT user_screen_name, {granular}, state, created_at, tweet FROM hashtag_{tableQuery}
                                                where state = '{input_state_full}')
                                        SELECT user_screen_name, {granular}, state, created_at, tweet FROM stateTweetData
                                        WHERE {granular} = (SELECT MAX({granular}) FROM stateTweetData);'
                            """

                            # print(query)
                            query_content.execute(query)

                            results = query_content.fetchall()

                            # print(results)
                            name, granular_val, state, created_at, tweet = results[0]

                            if not name or not granular_val or not created_at or not tweet:
                                raise Exception("Sorry, an error occurred and it failed to grab the metadata.")

                            if not state:
                                state = "USA"

                            reword = ""
                            if granular == "followers":
                                reword = " from user"

                            print("The tweet about " + candidate + reword + " with the most " + granular + " of a count of " + str(granular_val) + " in " + input_state_full + " is: ")
                            print("\"" + tweet + "\"")
                            print("The tweet was made by " + name + ", posted in "  + state + " at " + created_at.strftime("%c"))
            else:

                if input_state not in state_name_data:
                    raise Exception("Sorry, incorrect state abbreviation.")

                input_state_full = state_name_data[input_state]
                print("Selected state: " + state_name_data[input_state])

                tableQuery = "joebiden" if candidate == "Joe Biden" else "donaldtrump"

                query = f"""SELECT count(*) FROM hashtag_{tableQuery} 
                        WHERE state = '{input_state_full}';
                """

                query_content.execute(query)

                results = query_content.fetchall()

                placeholder = str(results[0][0])

                print("The number of tweets about " + candidate + " in " + input_state_full + " is " + placeholder)
        elif (input_action == "demographics"):

            print("Determining: " + input_action)

            # talk about differentials from '16 to '20, and % of population that voted based on a demographic
            if args.granular:
                granular = args.granular.lower()

                granular_options = ["covid","men","women","hispanic","white","black","native","asian","pacific",
                "poverty","childpoverty","votingagecitizen", "income", "professional", "service", "office",
                "construction", "production", "drive", "carpool", "transit", "walk", "othertransp","workathome",
                "meancommute","employed","privatework","publicwork","selfemployed","familywork","unemployment"]

                gender_granular = ["men", "women"]
                ethnic_granular = ["hispanic","white","black","native","asian","pacific"]
                wealth_granular = ["poverty","childpoverty","votingagecitizen", "income"]
                occupation_granular = ["professional", "service", "office","construction", "production"]
                transportation_granular = ["drive", "carpool", "transit", "walk", "othertransp","workathome","meancommute"]
                employment_granular = ["employed","privatework","publicwork","selfemployed","familywork","unemployment"]

                query = ""
            else:
                query = ""

        # f.close()
