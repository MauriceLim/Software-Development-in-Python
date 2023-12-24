"""Invoke engine.py for various assumptions used in your analysis"""
import requests
import argparse
import mysql.connector
from mysql.connector import MySQLConnection, Error as MySQLError


import engine

ROOT_URL = "http://127.0.0.1:8000"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("assumption_id", type=int, choices=range(1,4), help="id for assumptions (1-3)")
    parser.add_argument("scenario_id", type=int, choices=range(1,4), help="id for scenarios (1-3)")
    parser.add_argument("parameter_id", type=int, choices=range(1,7), help="id for parameters (1-6)")
    parser.add_argument("policy_id", nargs = '?', choices=range(1,11), type=int, help="if id (1-10) not selected, model will run against all policies")
    args = parser.parse_args()
    
    assumption = requests.get(f"{ROOT_URL}/assumptions/{args.assumption_id}").json()
    scenario = requests.get(f"{ROOT_URL}/scenario/{args.scenario_id}").json()
    parameter = requests.get(f"{ROOT_URL}/parameters/{args.parameter_id}").json()
    mortality = requests.get(f"{ROOT_URL}/mortality").json()

    if args.policy_id is None:
        policy = requests.get(f"{ROOT_URL}/policies").json()
    else:
        policy = requests.get(f"{ROOT_URL}/policies/{args.policy_id}").json()
    
    input_data = engine.GMWB_pricing(assumption,scenario,parameter,policy,mortality)

    conn: MySQLConnection = mysql.connector.connect(
            user="root", host="0.0.0.0", port="3306", database = "zen_nilpferd"
        )
   
    scenario_id = args.scenario_id
    assumption_id = args.assumption_id
    parameter_id = args.parameter_id
    try:
        cursor = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            scenario_id INT,
            assumption_id INT,
            parameter_id INT,
            policy_id INT,
            cost FLOAT
        );
        """
        cursor.execute(create_table_query)

        alter_table_query = """
        ALTER TABLE results
        MODIFY COLUMN id INT AUTO_INCREMENT;
        """
        cursor.execute(alter_table_query)

        # Insert data into the "results" table
        insert_query = """
        INSERT INTO results (scenario_id, assumption_id, parameter_id, policy_id, cost)
        VALUES (%s, %s, %s, %s, %s);
        """

        # Iterate over the input data and insert into the database
        for policy_id, cost in input_data:
            cursor.execute(insert_query, (scenario_id, assumption_id, parameter_id, policy_id, float(cost)))

        # Commit the changes
        conn.commit()
        
        print("Data inserted successfully!")

    except MySQLError as e:
        print(f"Error: {e}")
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()


if __name__ == "__main__": 
    main()