import os
from fuzzworks import Fuzzworks
from src import get_nevekit_home

SDE_DB_NAME = "sde.db"


# Placeholder for SDE implementation
class SDE:
    def __init__(self, db_conn_str=None):
        """
        Initialize SDE object.

        :param db_conn_str: Connection string to the SDE db.
        """
        self.db_conn_str = db_conn_str

    def _download_db(self, db_path):
        """
        Fetch the Fuzzworks SDE SQLite db.

        :param db_path: Path to the SQLite db to create.
        :return: The created db's connection string.

        ## Doctest
        ### Download the Fuzzworks SDE SQLite db
        >>> sde = SDE()
        >>> sde._download_db('sde.db')
        'sqlite:///sde.db'
        """
        # Create the SQLite DB if it doesn't exist.
        if not os.path.exists(db_path):
            f = Fuzzworks()
            f.download_fuzzworks_sde_db(db_path=db_path)

        # Return the connection string to the SQLite DB.
        return f"sqlite:///{db_path}"

    def init(self):
        """
        Setup SQLite DB for SDE data.
        """
        # SDE Data is stored in a SQLite database in the ~/.nevekit folder.
        db_path = f"{get_nevekit_home()}/{SDE_DB_NAME}"
        self.db_conn_str = self._download_db(db_path)
