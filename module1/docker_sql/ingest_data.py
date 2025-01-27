import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import subprocess
import os


def main(params):
    print("Downloading file...")

    result = subprocess.run(
        ["wget", params.url],
        capture_output=True,
        text=True,
    )

    # Parse the output to get the filename
    # Assuming the filename is in the last line of stderr and follows 'Saving to: ' or similar
    output_lines = filter(lambda x: "Saving to:" in x, result.stderr.splitlines())
    file_name = next(output_lines).split("‘")[1].split("’")[0]

    # unzip the file if necessary
    if file_name.endswith(".gz"):
        if os.path.exists(file_name.replace(".gz", "")):
            os.remove(file_name.replace(".gz", ""))
        subprocess.run(["gunzip", file_name])
        file_name = file_name.replace(".gz", "")

    print("File downloaded:", file_name)

    engine = create_engine(
        f"postgresql://{params.user}:{params.password}@{params.host}:{params.port}/{params.database}"
    )

    df_iter = pd.read_csv(
        file_name, iterator=True, chunksize=100000, encoding="utf8"
    )  # Shift + Tab to open function doc

    df = next(df_iter)

    # convert datetime again since we loaded the csv file again
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # before inserting any data, we will insert 0 rows (only the header) so that postgres creates the table.
    df.head(0).to_sql(
        name=params.table, con=engine, if_exists="replace"
    )  # iif a table with the same name already exists, replace it

    df.to_sql(name=params.table, con=engine, if_exists="append")

    print("\nTable created. Inserting data...\n")

    for df in df_iter:
        t_start = time()

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(
            name=params.table, con=engine, if_exists="append"
        )  # now we want to append the data to the existing table

        print(f"Loaded a chunk... took {time() - t_start} seconds...")

    print("\n\nData inserted.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    # parameters to ask the user for:
    # user
    # password
    # host
    # port
    # database name
    # table name
    # url of the csv file

    parser.add_argument("--user", required=True, help="user name for postgres")
    parser.add_argument("--password", required=True, help="password for postgres")
    parser.add_argument("--host", required=True, help="host for postgres")
    parser.add_argument("--port", required=True, help="port for postgres")
    parser.add_argument("--database", required=True, help="database name for postgres")
    parser.add_argument(
        "--table",
        required=True,
        help="name of the table where data should be written to",
    )
    parser.add_argument("--url", required=True, help="url of the csv file")

    args = parser.parse_args()

    main(args)
