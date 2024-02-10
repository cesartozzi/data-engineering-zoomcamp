import os
import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse



def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    if url.endswith('.csv.gz'):
        file_name = 'output.csv.gz'
    elif url.endswith('.parquet'):
        file_name = 'output.parquet'
    else:
        file_name = 'output.csv'

    os.system(f"wget {url} -O {file_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    if url.endswith('.parquet'):
        df = pd.read_parquet(file_name)
        file_name = 'output.csv.gz'
        df.to_csv(file_name, index=False, compression="gzip")

    df_iter = pd.read_csv(file_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:

        try:
            t_start = time()
            df = next(df_iter)

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk..., took %.3f seconds' % (t_end - t_start))
        except StopIteration:
            print("Finished ingesting data into postgres database")
            break

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest csv data into a postgres database.')

    parser.add_argument('--user', help='user for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='post for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the database table where the data will be stored')
    parser.add_argument('--url', help='url of the csv file to be ingested')

    args = parser.parse_args()
    
    main(args)
