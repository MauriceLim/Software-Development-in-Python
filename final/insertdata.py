import csv
import os
import mysql.connector
from mysql.connector import MySQLConnection

def insert_csv_data_into_mysql(csv_path, table_name, conn: MySQLConnection, column_names):
    cursor = conn.cursor()

    with open(csv_path, 'r') as csvfile:
        csv_data = csv.reader(csvfile)
        next(csv_data)
        for row in csv_data:
            placeholders = ', '.join(['%s' for _ in row])
            insert_query = f'INSERT INTO {table_name} ({", ".join(column_names)}) VALUES ({placeholders})'
            cursor.execute(insert_query, row)

    # Commit changes and close the cursor
    conn.commit()
    cursor.close()

    print(f"Inserted data from {csv_path} into {table_name}")

def main():
    conn: MySQLConnection = mysql.connector.connect(
        user="root", host="0.0.0.0", port="3306", database = "zen_nilpferd"
    )

    # Example for each CSV file and corresponding table
    csv_folder = 'db'
    csv_files = ['assumptions.csv', 'mortality.csv', 'parameters.csv', 'policies.csv', 'scenarios.csv']
    table_names = ['assumptions', 'mortality', 'parameters', 'policies', 'scenarios']
    column_names_list = [['id', 'mortality_multiplier', 'wd_age', 'min_wd_delay', 'record_description'],
                         ['age', 'qx'],
                         ['id', 'proj_periods', 'num_paths', 'seed', 'record_description'],
                         ['id', 'issue_age', 'initial_premium', 'fee_pct_av', 'benefit_type', 'ratchet_type', 'guarantee_wd_rate'],
                         ['id', 'risk_free_rate', 'dividend_yield', 'volatility', 'record_description']]

    for csv_file, table_name, column_names in zip(csv_files, table_names, column_names_list):
        csv_path = os.path.join(csv_folder, csv_file)
        insert_csv_data_into_mysql(csv_path, table_name, conn, column_names)

    conn.close()

if __name__ == "__main__":
    main()
