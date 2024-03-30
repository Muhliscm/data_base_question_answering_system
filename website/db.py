# from langchain.utilities import SQLDatabase
from langchain_community.utilities import SQLDatabase
import pymysql
import os
from dotenv import load_dotenv


load_dotenv()
google_api_key = os.environ["GOOGLE_API_KEY"]
username = os.environ["username"]
password = os.environ["password"]
host = os.environ["host"]
database = os.environ["database"]


def connect_db():

    try:
        db = SQLDatabase.from_uri(
            f"mysql+pymysql://{username}:{password}@{host}/{database}",
            sample_rows_in_table_info=3,
        )
    except Exception as ex:
        print("Exception occurred in generating db object", ex)
        db = ""

    return db


if __name__ == "__main__":
    db = connect_db()
    print(db.table_info)
