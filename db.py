# from langchain.utilities import SQLDatabase
from langchain_community.utilities import SQLDatabase
import pymysql


def connect_db():
    username = "root"
    password = "root"
    host = "localhost"
    database = "atliq_tshirts"
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
