import argparse
import mysql.connector
import configparser
import json
import datetime
import unittest

#config.ini parser
config = configparser.ConfigParser()
config.read('./config.ini')

# replace password with actual password, can now run queries and see results!
cnx = mysql.connector.connect(user=config['MYSQL']['USER'], password=config['MYSQL']['PASSWORD'], host=config['MYSQL']['HOST'], port=config['MYSQL']['PORT'], database=config['MYSQL']['DATABASE'])
query_content = cnx.cursor()

class TestDatabaseQueries(unittest.TestCase):
    # A basic query to verify the Trump Tweets dataset by scanning the entire table for the earliest tweet and returing relevant metadata
    def test_basic_tweet_query_trump(self):        
        tweet_query = """SELECT * FROM hashtag_donaldtrump ORDER BY 
                        created_at ASC LIMIT 1
                        """
        query_content.execute(tweet_query)
        result = query_content.fetchall()
        # We know the earliest tweet to be Oct 15, 2020
        self.assertEqual(str(result[0][0]), '2020-10-15 00:00:01')

    # A basic query to verify the Biden Tweets dataset by scanning the entire table for the latest tweet and returing relevant metadata
    def test_basic_tweet_query_biden(self):        
        tweet_query = """SELECT * FROM hashtag_joebiden ORDER BY 
                        created_at DESC LIMIT 1
                        """
        query_content.execute(tweet_query)
        result = query_content.fetchall()
        # We know the latest tweet to be Nov 8, 2020
        self.assertEqual(str(result[0][0]), '2020-11-08 23:59:58')

    # The following test is designed to sum the votes in all counties of a state, which should be roughly equivalent to the total votes of that state.
    # Due to a small margin of human error in the voting process and dataset, we introduce a 2% error rate. 
    # However, there are many states that are not represented in the electoral process which are removed.
    # Moreover, due to limitations of the dataset, there are many missing counties from Illinois and Alaska, which leads to inaccurate numbers 
    # Resultantly these states are removed from the set 
    def test_county_state_votes_(self):
        with open('./US_states.json') as f:
            state_name_data = json.load(f)
            unrepresented_states = ['AK', 'AS', 'FM', 'GU', 'IL', 'MH', 'MP', 'PW', 'PR', 'VI']
            for key in unrepresented_states:
                state_name_data.pop(key)
            
            for state in state_name_data.values():
                test_state = state
                # print(test_state)
                sum_counties_query = f"""SELECT SUM(total_votes) FROM president_county_candidate WHERE 
                                    state = '{test_state}'
                                    """
                query_content.execute(sum_counties_query)
                result = query_content.fetchall()

                sum_votes_counties = result[0][0]

                votes_state_query = f"""SELECT votes FROM president_state WHERE
                                    state = '{test_state}'
                                    """
                query_content.execute(votes_state_query)

                result = query_content.fetchall()
                votes_state = result[0][0]

                # We introduce an error rate of 2%, this is due to the fact that the data 
                delta = (0.02)*float((sum_votes_counties + votes_state)/2)
                self.assertAlmostEqual(sum_votes_counties, votes_state, None, None, delta)

    # The test verifies that the client program can properly handle adding annotations to the county_statistics dataset.
    # This is accomplished by creating a test annotation and verifying that the annotation then appears in the mysql database
    def test_annotation(self):
        with open('./US_states.json') as f:
            note = "test_annotation"
            test_state = "CA"
            test_county = "Los Angeles"
            annotation_query = f"""UPDATE county_statistics
                            SET notes = '{note}'
                            WHERE state = '{test_state}' AND
                            county = '{test_county}'
                """
            query_content.execute(annotation_query)
            cnx.commit()

            find_new_annotation = f"""SELECT notes FROM county_statistics
                            WHERE state = '{test_state}' AND
                            county = '{test_county}'
            """
            query_content.execute(find_new_annotation)
            result = query_content.fetchall()
            self.assertEqual(result[0][0], note)

if __name__ == '__main__':
    unittest.main()