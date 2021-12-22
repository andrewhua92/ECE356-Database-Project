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
parser.add_argument('-c', '--county', help="Enter the county you would like to know about or reference.")
parser.add_argument('-p', '--presidental_candidate', help="The candidate that you would like to know about. Please use 'jb' for Joe Biden or 'dt' for Donald Trump.")
parser.add_argument('-g', '--granular', help="Specifies specific property to look up in different actions.")
parser.add_argument('-d', '--date', default="20", help="Year that will be used for checking polling data.")
parser.add_argument('-n', '--note', help="Used to append a note to a county to store in the database.")
parser.add_argument('-r', '--remove', action='store_true',help="Pass this flag in conjunction with the append function to remove the referenced note for current county.")
parser.set_defaults(remove=False)
args = parser.parse_args()

# where the magic happens. the main that runs everything
if __name__ == "__main__":
    if args.state:
        input_state = args.state.upper()
    else:
        input_state = None
    if args.presidental_candidate:
        temp = args.presidental_candidate.lower()
        if temp == "jb":
            presidental_candidate = "Joe Biden"
        else:
            presidental_candidate = "Donald Trump"
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

        # Input action: loser
        # Flags: -s
        # Determines the loser of a specific state
        if (input_action == "loser"):
            if input_state and input_state not in state_name_data:
                raise Exception("Sorry, incorrect state abbreviation.")
            elif not input_state:
                print("Loser of the 2020 US election was Donald Trump.")
                exit()

            input_state_full = state_name_data[input_state]
            print("Selected state: " + state_name_data[input_state])

            print("Determining: " + input_action)

            query = f"""WITH voteCount AS
                            (SELECT candidate, SUM(total_votes) AS votes FROM President_county_candidate WHERE
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

            # cheeky piece of code since we either will have Joe or Donald as a winner... 
            # so a winner is simply the complement of the other
            if (placeholder == "Joe Biden"):
                placeholder = "Donald Trump"
            else:
                placeholder = "Joe Biden"

            print("Loser in " + input_state_full + " is " + placeholder)
        
        # Input action: winner
        # Flags: -s
        # Determines the inner of a specific state
        elif (input_action == "winner"):
            if input_state and input_state not in state_name_data:
                raise Exception("Sorry, incorrect state abbreviation.")
            elif not input_state:
                print("Winner of the 2020 US election was Joe Biden.")
                exit()

            input_state_full = state_name_data[input_state]
            print("Selected state: " + state_name_data[input_state])

            print("Determining: " + input_action)

            query = f"""WITH voteCount AS
                            (SELECT candidate, SUM(total_votes) AS votes FROM President_county_candidate WHERE
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

        # Input action: tweets
        # Flags: -p, -g (optional), -s (optional)
        # Provides information about a specific candidate (Joe or Donald)
        # Can lower scope to the state level
        # Can be explicit in determining the 'most' of a property of a tweet (i.e. likes, retweets, etc)
        elif (input_action == "tweets"):

            print("Determining: " + input_action) 

            if not args.presidental_candidate:
                raise Exception("Sorry, no candidate provided for tweet information. Please use -h for more info.")

            if args.granular:
                granular = args.granular

                tableQuery = "joebiden" if presidental_candidate == "Joe Biden" else "donaldtrump"

                granular_options = ["likes", "retweets", "followers", "country", "continent", "city", "state"]
                metadata_options = ["likes", "retweets", "followers"]
                location_options = ["country", "continent", "city", "state"]

                if granular in granular_options:
                    if granular in metadata_options:
                        if not args.state: 
                            query = f""" SELECT user_screen_name, {granular}, state, created_at, tweet FROM Hashtag_{tableQuery}
                                WHERE {granular} = (SELECT MAX({granular}) FROM Hashtag_{tableQuery})
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

                            print("The tweet about " + presidental_candidate + reword + " with the most " + granular + " of a count of " + str(granular_val) + " is: ")
                            print("\"" + tweet + "\"")
                            print("The tweet was made by " + name + ", posted in " + state + " at " + created_at.strftime("%c"))
                        else:

                            if input_state not in state_name_data:
                                raise Exception("Sorry, incorrect state abbreviation.")

                            input_state_full = state_name_data[input_state]
                            print("Selected state: " + state_name_data[input_state])

                            query = f"""WITH stateTweetData AS
                                            (SELECT user_screen_name, {granular}, state, created_at, tweet FROM Hashtag_{tableQuery}
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

                            print("The tweet about " + presidental_candidate + reword + " with the most " + granular + " of a count of " + str(granular_val) + " in " + input_state_full + " is: ")
                            print("\"" + tweet + "\"")
                            print("The tweet was made by " + name + ", posted in "  + state + " at " + created_at.strftime("%c"))
            else:
                if input_state not in state_name_data:
                    raise Exception("Sorry, incorrect state abbreviation.")

                input_state_full = state_name_data[input_state]
                print("Selected state: " + state_name_data[input_state])

                tableQuery = "joebiden" if presidental_candidate == "Joe Biden" else "donaldtrump"

                query = f"""SELECT count(*) FROM Hashtag_{tableQuery} 
                        WHERE state = '{input_state_full}';
                """

                query_content.execute(query)

                results = query_content.fetchall()

                placeholder = str(results[0][0])

                print("The number of tweets about " + presidental_candidate + " in " + input_state_full + " is " + placeholder)

        # Input action: demographics
        # Flags: -g, -s
        # Figures out on a state-wide level the representation of a voting population of a demographic
        # Also always includes historic data to supplement the demographic information
        elif (input_action == "demographics"):

            print("Determining: " + input_action)

            if input_state not in state_name_data:
                raise Exception("Sorry, incorrect state abbreviation.")

            input_state_full = state_name_data[input_state]
            print("Selected state: " + state_name_data[input_state])

            # talk about differentials from '16 to '20, and % of population that voted based on a demographic
            if args.granular:
                granular = args.granular.lower()

                granular_options = ["cases","deaths","men","women","hispanic","white","black","native","asian","pacific",
                "poverty","childpoverty","votingagecitizen", "income", "incomeerr", "incomepercap", "incomepercaperr", "professional", 
                "service", "office", "construction", "production", "drive", "carpool", "transit", "walk", "othertransp",
                "workathome", "meancommute","employed","privatework","publicwork","selfemployed","familywork","unemployment"]

                covid_granular = ["cases", "deaths"]
                gender_granular = ["men", "women"]
                ethnic_granular = ["hispanic","white","black","native","asian","pacific"]
                wealth_granular = ["poverty","childpoverty"]
                income_granular = ["income", "incomeerr", "incomepercap", "incomepercaperr"]
                occupation_granular = ["professional", "service", "office","construction", "production"]
                transportation_granular = ["drive", "carpool", "transit", "walk", "othertransp","workathome","meancommute"]
                employment_granular = ["employed","privatework","publicwork","selfemployed","familywork","unemployment"]

                granular_query = ""
                if granular == "votingagecitizen" or granular in covid_granular or granular == "employed":
                    granular_query = f"SUM({granular})"
                elif granular in ethnic_granular or granular in occupation_granular or granular in transportation_granular or granular in employment_granular or granular in wealth_granular or granular in income_granular:
                    granular_query = f"AVG({granular})"
                elif granular in gender_granular:
                    granular_query = f"(SUM({granular}) / SUM(TotalPop) * 100)"
                
                query1 = f"""SELECT AVG(percentage20_Donald_Trump),
                        AVG(percentage16_Donald_Trump),
                        (AVG(percentage20_Donald_Trump) - AVG(percentage16_Donald_Trump)) * 100 as Rep_pct, 
                        AVG(percentage20_Joe_Biden),
                        AVG(percentage16_Hillary_Clinton),
                        (AVG(percentage20_Joe_Biden)-AVG(percentage16_Hillary_Clinton)) * 100 as Dem_pct,
                        AVG(votes20_Donald_Trump),
                        AVG(votes16_Donald_Trump), 
                        (SUM(votes20_Donald_Trump) - SUM(votes16_Donald_Trump)) as Rep_votes, 
                        AVG(votes20_Joe_Biden),
                        AVG(votes16_Hillary_Clinton),
                        (SUM(votes20_Joe_Biden)-SUM(votes16_Hillary_Clinton)) as Dem_votes
                        FROM County_statistics 
                        WHERE state = '{input_state}' 
                """

                query_content.execute(query1)

                results1 = query_content.fetchall()

                avg_rep_pct_20, avg_rep_pct_16, avg_rep_pct_diff, avg_dem_pct_20, avg_dem_pct_16, avg_dem_pct_diff, avg_rep_votes_20,avg_rep_votes_16,\
                avg_rep_votes_diff, avg_dem_votes_20, avg_dem_votes_16, avg_dem_votes_diff = results1[0]

                query2 = f"""SELECT {granular_query} FROM Demographics 
                        WHERE state = '{input_state}'
                """

                query_content.execute(query2)

                results2 = query_content.fetchall()

                granular_pct = results2[0][0]

                if granular == "votingagecitizen":
                    print("For the US 2020 Election, there were " + str(granular_pct) + " voting age citizens in the state of " + input_state_full)
                elif granular == "employed":
                    print("For the US 2020 Election, there were " + str(granular_pct) + " employed individuals in the state of " + input_state_full)
                elif granular == "meancommute":
                    print("For the US 2020 Election, the mean commute was " + str(granular_pct) + " minutes in the state of " + input_state_full)
                elif granular in covid_granular:
                    print("For the US 2020 Election, there were " + str(granular_pct) + " COVID " + granular + " in the state of " + input_state_full)
                elif granular in income_granular:
                    print("For the US 2020 Election, here is the average " + granular + ": " + str(granular_pct) + " in the state of " + input_state_full)
                elif granular in wealth_granular:
                    print("For the US 2020 Election, here is the average " + granular + " rate: " + str(granular_pct) + " in the state of " + input_state_full)
                elif granular in ethnic_granular or granular in occupation_granular or granular in transportation_granular or granular in employment_granular:
                    print("For the US 2020 Election, the " + granular + " demographic votes in " + input_state_full + " represented " + str(granular_pct) + "% of all votes.")
                elif granular in gender_granular:
                    print("For the US 2020 Election, votes by " + granular + " in " + input_state_full + " represented " + str(granular_pct) + "% of all votes.")


                print("Overall, here are some statistics of differences in voting turnout given the above demographic.")
                print("Note, these are on an average county basis for the state of " + input_state_full)
                print("Average percentage of voters for Republicans in 2020: " + str(avg_rep_pct_20) + " %.")
                print("Average percentage of voters for Republicans in 2016: " + str(avg_rep_pct_16) + " %.")
                print("Average percentage of voters for Republicans difference: " + str(avg_rep_pct_diff) + " %.")
                print("Average percentage of voters for Democrats in 2020: " + str(avg_dem_pct_20) + " %.")
                print("Average percentage of voters for Democrats in 2016: " + str(avg_dem_pct_16) + " %.")
                print("Average percentage of voters for Democrats difference: " + str(avg_dem_pct_diff) + " %.")
                print("Average number of voters for Republicans in 2020: " + str(avg_rep_votes_20) + ".")
                print("Average number of voters for Republicans in 2016: " + str(avg_rep_votes_16) + ".")
                print("Average number of voters for Republicans difference: " + str(avg_rep_votes_diff) + ".")
                print("Average number of voters for Democrats in 2020: " + str(avg_dem_votes_20) + ".")
                print("Average number of voters for Democrats in 2016: " + str(avg_dem_votes_16) + ".")
                print("Average number of voters for Democrats difference: " + str(avg_dem_votes_diff) + ".")

            # this will only consider voting % differences (which can help see differences) 
            else:
                raise Exception("Wrong type of demographic.")

        # Input action: polling
        # Flags: -s, -d (optional)
        # Provides the polling data for a state in percentages and vote count, including comparison to the 2016 election
        elif (input_action == "polling"):

            if input_state not in state_name_data:
                raise Exception("Sorry, incorrect state abbreviation.")

            input_state_full = state_name_data[input_state]

            print("Determining: " + input_action)

            print("Selected state: " + state_name_data[input_state])

            if args.date == "20":
            
                query=f"""SELECT candidate_name, sum(sample_size * pct / 10) FROM Trump_biden_polls
                    WHERE state = '{input_state_full}' 
                    GROUP BY candidate_name
                    ORDER BY SUM(sample_size*pct/10) desc limit 3
                """

                query_content.execute(query)

                results = query_content.fetchall()

                print("Polling data for the US 2020 Election in " + input_state_full + " across all polls, in descending order of votes.")

                for result in results:
                    name, votes = result
                    votes = round(votes)
                    print(name + " with " + str(votes) + " votes")
            elif args.date == "16":
                query=f"""SELECT SUM(clinton_pct*sample_size) as Clinton, SUM(trump_pct*sample_size) as Trump FROM Trump_clinton_polls
                    WHERE state = '{input_state_full}'
                """

                query_content.execute(query)

                results = query_content.fetchall()

                clintonVotes = results[0][0]
                clintonVotes = round(clintonVotes)
                trumpVotes = results[0][1]
                trumpVotes = round(trumpVotes)

                print("Polling data for the US 2016 Election in " + input_state_full + " across all polls.")
                print("Donald Trump with " + str(trumpVotes) + " votes.")
                print("Hillary Clinton with " + str(clintonVotes) + " votes.")
            else:
                raise Exception("Invalid date for polling information. Please use either 16 or 20.")
        
        elif (input_action == "annotate"):
            if input_state not in state_name_data:
                raise Exception("Sorry, incorrect state abbreviation.")

            input_state_full = state_name_data[input_state]

            print("Determining: " + input_action)

            print("Selected state: " + state_name_data[input_state])

            if args.remove:
                
                query = f"""UPDATE County_statistics
                            SET notes = ""
                            WHERE state = '{input_state}' AND
                            county = '{args.county}'
                """

                query_content.execute(query)

                cnx.commit()

                print(query_content.rowcount, "record(s) affected.")

            else:

                if len(args.note) > 255:
                    raise Exception("Note is too long! Please use a smaller note.")

                query = f"""UPDATE County_statistics
                            SET notes = '{args.note}'
                            WHERE state = '{input_state}' AND
                            county = '{args.county}'
                """

                query_content.execute(query)

                cnx.commit()

                print(query_content.rowcount, "record(s) affected.")
            
        elif (input_action == "county"):
            if input_state not in state_name_data:
                raise Exception("Sorry, incorrect state abbreviation.")

            input_state_full = state_name_data[input_state]

            print("Determining: " + input_action)

            print("Selected state: " + state_name_data[input_state])

            if args.granular == "demographics" or args.granular == "all":

                query1 = f"""SELECT * FROM Demographics
                        WHERE state = '{input_state}' and
                        county = '{args.county}'
                """
                query_content.execute(query1)

                # print(query1)
                results = query_content.fetchall()
                # print(results)

                if not results:
                    raise Exception("Likely an incorrectly spelled county name. Please try again.")
                
                c_county, c_state, c_cases, c_deaths, c_pop, c_men, c_women, c_hispanic, c_white, c_black,\
                c_native, c_asian, c_pacific, c_vac, c_income, c_income_err, c_ipc, c_ipce, c_poverty, c_child_poverty,\
                c_professional, c_service, c_office, c_construction, c_production, c_drive, c_carpool, c_transit, c_walk,\
                c_othertransp, c_wfh, c_meancommute, c_employed, c_private_work, c_public_work, c_self_employed,\
                c_family_work, c_unemployment = results[0]

                print("Demographic Information for " + args.county + " located in " + input_state_full)
                print("Number of COVID-19 cases: " + str(c_cases))
                print("Number of COVID-19 deaths: " + str(c_deaths))
                print("Total population: " + str(c_pop))
                print("Population of men: " + str(c_men))
                print("Population of women: " + str(c_women))
                print("Population percent of Hispanic: " + str(c_hispanic) + "%")
                print("Population percent of White: " + str(c_white) + "%")
                print("Population percent of Black: " + str(c_black) + "%")
                print("Population percent of Native: " + str(c_native) + "%")
                print("Population percent of Asian: " + str(c_asian) + "%")
                print("Population percent of Pacific: " + str(c_pacific) + "%")
                print("Number of voting citizens: " + str(c_vac))
                print("Average Income: $" + str(c_income))
                print("Average Income Error: $" + str(c_income_err))
                print("Income Per Capita: $" + str(c_ipc))
                print("Income Per Capita Error: $" + str(c_ipce))
                print("Average poverty rate: " + str(c_poverty) + "%")
                print("Average poverty rate in children: " + str(c_child_poverty) + "%")
                print("Population percent of professional workers: " + str(c_professional) + "%")
                print("Population percent of service workers: " + str(c_service) + "%")
                print("Population percent of office workers: " + str(c_office) + "%")
                print("Population percent of construction workers: " + str(c_construction) + "%")
                print("Population percent of production workers: " + str(c_production) + "%")
                print("Population percent that drive: " + str(c_drive) + "%")
                print("Population percent that carpool: " + str(c_carpool) + "%")
                print("Population percent that use transit: " + str(c_transit) + "%")
                print("Population percent that walk: " + str(c_walk) + "%")
                print("Population percent that use other transportation: " + str(c_othertransp) + "%")
                print("Population percent that work from home: " + str(c_wfh) + "%")
                print("Mean commute time in minutes: " + str(c_meancommute) + " minutes")
                print("Number of currently employed individuals: " + str(c_employed))
                print("Population percent in private work: " + str(c_private_work) + "%")
                print("Population percent in public work: " + str(c_public_work) + "%")
                print("Population percent that is self-employed: " + str(c_self_employed) + "%")
                print("Population percent in family work: " + str(c_family_work) + "%")
                print("Population percent in unemployment: " + str(c_unemployment) + "%")
                print()

            if args.granular == "historic" or args.granular == "all":

                query2 = f"""SELECT * FROM County_statistics
                        WHERE state = '{input_state}' and
                        county = '{args.county}'
                
                """

                query_content.execute(query2)

                results = query_content.fetchall()
                # print(results)

                c_county, c_state, pct16_rep, pct16_dem, votes16, votes16_rep, votes16_dem, pct20_rep, pct20_dem,\
                votes20, votes20_rep, votes20_dem, c_lat, c_lng, c_notes = results[0]

                print("Historic information of " + args.county  + " located in " + input_state_full)
                print("Percentage of voters for Democrats in 2020: " + str(pct20_dem) + " %.")
                print("Percentage of voters for Republicans in 2020: " + str(pct20_rep) + " %.")
                print("Percentage of voters for Democrats in 2016: " + str(pct16_dem) + " %.")
                print("Percentage of voters for Republicans in 2016: " + str(pct16_rep) + " %.")
                print("Total of voters in " + args.county + " in 2020: " + str(votes20) + ".")
                print("Number of voters for Democrats in 2020: " + str(votes20_dem) + ".")
                print("Number of voters for Republicans in 2020: " + str(votes20_rep) + ".")
                print("Total of voters in " + args.county + " in 2016: " + str(votes16) + ".")
                print("Number of voters for Democrats in 2016: " + str(votes16_dem) + ".")
                print("Number of voters for Republicans in 2016: " + str(votes16_rep) + ".")
                print("Latitude: " + str(c_lat))
                print("Longitutde: " + str(c_lng))
                print("Notes: " + c_notes)

            elif not args.granular:

                query = f"""SELECT lat, lng, notes FROM County_statistics
                        WHERE state = '{input_state}' and
                        county = '{args.county}'
                """

                query_content.execute(query)

                results = query_content.fetchall()

                if not results:
                    raise Exception("Likely an incorrectly spelled county name. Please try again.")

                c_lat, c_lng, c_notes = results[0]

                print("County Information on : " + args.county + " located in " + input_state_full)
                print("Latitude: " + str(c_lat))
                print("Longitutde: " + str(c_lng))
                print("Notes: " + c_notes)
            

        elif (input_action == "state"):
            if input_state not in state_name_data:
                raise Exception("Sorry, incorrect state abbreviation.")

            input_state_full = state_name_data[input_state]

            print("Determining: " + input_action)

            print("Selected state: " + state_name_data[input_state])

            if args.granular != "historic" and args.granular != "demographics" and args.granular != "all":
                raise Exception("Incorrect granularity. Must select one for the state level. Please select from either historic, demographics, or all.")

            if args.granular == "demographics" or args.granular == "all":

                query1 = f"""SELECT state, SUM(cases), SUM(deaths), SUM(TotalPop), SUM(Men), SUM(Women), AVG(Hispanic), AVG(White), AVG(Black), AVG(Native),
                    AVG(Asian), AVG(Pacific), SUM(VotingAgeCitizen), AVG(Income), AVG(IncomeErr), AVG(IncomePerCap), AVG(IncomePerCapErr), AVG(Poverty),
                    AVG(ChildPoverty), AVG(Professional), AVG(Service), AVG(Office), AVG(Construction), AVG(Production), AVG(Drive), AVG(Carpool),
                    AVG(Transit), AVG(Walk), AVG(OtherTransp), AVG(WorkAtHome), AVG(MeanCommute), SUM(Employed), AVG(PrivateWork), AVG(PublicWork),
                    AVG(SelfEmployed), AVG(FamilyWork), AVG(Unemployment) FROM Demographics WHERE state = "LA"
                """
                query_content.execute(query1)

                # print(query1)
                results = query_content.fetchall()
                # print(results)

                c_state, c_cases, c_deaths, c_pop, c_men, c_women, c_hispanic, c_white, c_black,\
                c_native, c_asian, c_pacific, c_vac, c_income, c_income_err, c_ipc, c_ipce, c_poverty, c_child_poverty,\
                c_professional, c_service, c_office, c_construction, c_production, c_drive, c_carpool, c_transit, c_walk,\
                c_othertransp, c_wfh, c_meancommute, c_employed, c_private_work, c_public_work, c_self_employed,\
                c_family_work, c_unemployment = results[0]

                print("Demographic Information averaged across counties for " + input_state_full)
                print("Number of COVID-19 cases: " + str(c_cases))
                print("Number of COVID-19 deaths: " + str(c_deaths))
                print("Total population: " + str(c_pop))
                print("Population of men: " + str(c_men))
                print("Population of women: " + str(c_women))
                print("Population percent of Hispanic: " + str(c_hispanic) + "%")
                print("Population percent of White: " + str(c_white) + "%")
                print("Population percent of Black: " + str(c_black) + "%")
                print("Population percent of Native: " + str(c_native) + "%")
                print("Population percent of Asian: " + str(c_asian) + "%")
                print("Population percent of Pacific: " + str(c_pacific) + "%")
                print("Number of voting citizens: " + str(c_vac))
                print("Average Income: $" + str(c_income))
                print("Average Income Error: $" + str(c_income_err))
                print("Income Per Capita: $" + str(c_ipc))
                print("Income Per Capita Error: $" + str(c_ipce))
                print("Average poverty rate: " + str(c_poverty) + "%")
                print("Average poverty rate in children: " + str(c_child_poverty) + "%")
                print("Population percent of professional workers: " + str(c_professional) + "%")
                print("Population percent of service workers: " + str(c_service) + "%")
                print("Population percent of office workers: " + str(c_office) + "%")
                print("Population percent of construction workers: " + str(c_construction) + "%")
                print("Population percent of production workers: " + str(c_production) + "%")
                print("Population percent that drive: " + str(c_drive) + "%")
                print("Population percent that carpool: " + str(c_carpool) + "%")
                print("Population percent that use transit: " + str(c_transit) + "%")
                print("Population percent that walk: " + str(c_walk) + "%")
                print("Population percent that use other transportation: " + str(c_othertransp) + "%")
                print("Population percent that work from home: " + str(c_wfh) + "%")
                print("Mean commute time in minutes: " + str(c_meancommute) + " minutes")
                print("Number of currently employed individuals: " + str(c_employed))
                print("Population percent in private work: " + str(c_private_work) + "%")
                print("Population percent in public work: " + str(c_public_work) + "%")
                print("Population percent that is self-employed: " + str(c_self_employed) + "%")
                print("Population percent in family work: " + str(c_family_work) + "%")
                print("Population percent in unemployment: " + str(c_unemployment) + "%")
                print()

            if args.granular == "historic" or args.granular == "all":

                query2 = f"""SELECT state, AVG(percentage16_Donald_Trump), AVG(percentage16_Hillary_Clinton), SUM(total_votes16), SUM(votes16_Donald_Trump),
                        SUM(votes16_Hillary_Clinton), AVG(percentage20_Donald_Trump), AVG(percentage20_Joe_Biden), SUM(total_votes20), SUM(votes20_Donald_Trump),
                        SUM(votes20_Joe_Biden) FROM County_statistics WHERE state = '{input_state}'
                
                """

                query_content.execute(query2)

                results = query_content.fetchall()
                # print(results)

                c_state, pct16_rep, pct16_dem, votes16, votes16_rep, votes16_dem, pct20_rep, pct20_dem,\
                votes20, votes20_rep, votes20_dem = results[0]

                print("Historic information averaged across counties from " + input_state_full)
                print("Percentage of voters for Democrats in 2020: " + str(pct20_dem) + " %.")
                print("Percentage of voters for Republicans in 2020: " + str(pct20_rep) + " %.")
                print("Percentage of voters for Democrats in 2016: " + str(pct16_dem) + " %.")
                print("Percentage of voters for Republicans in 2016: " + str(pct16_rep) + " %.")
                print("Total of voters in " + input_state_full + " in 2020: " + str(votes20) + ".")
                print("Number of voters for Democrats in 2020: " + str(votes20_dem) + ".")
                print("Number of voters for Republicans in 2020: " + str(votes20_rep) + ".")
                print("Total of voters in " + input_state_full + " in 2016: " + str(votes16) + ".")
                print("Number of voters for Democrats in 2016: " + str(votes16_dem) + ".")
                print("Number of voters for Republicans in 2016: " + str(votes16_rep) + ".")

           
        # f.close()
