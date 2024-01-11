import requests

from src import logger

DB_TYPE_TO_FUZZWORKS_ENDPOINT = {
    "sqlite": "dump/sqlite-latest.sqlite.bz2",
    "postgres": "dump/postgres-latest.dmp.bz2",
    "mysql": "dump/mysql-latest.dmp.bz2",
}


class Fuzzworks:
    BASE_URL = "https://www.fuzzwork.co.uk"

    def __init__(self):
        pass

    def fetch_data(self, endpoint):
        """
        Generic method to fetch data from a Fuzzworks endpoint.
        :param endpoint: Specific endpoint to fetch data from.
        :return: Fetched data in a processed format.

        ## Doctest
        ### Fetch data from an endpoint
        >>> fuzzworks = Fuzzworks()
        >>> fuzzworks.fetch_data('dump/lpOffers.txt')
        <Response [200]>
        """
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.get(url)
        response.raise_for_status()
        return response

    def download_fuzzworks_sde_db(self, db_path, db_type="sqlite"):
        """
        Download a Fuzzworks SDE db and save it to the specified path.

        :param db_path: Path to save the downloaded db to.

        ## Doctest
        ### Download a Fuzzworks SDE db
        >>> fuzzworks = Fuzzworks()
        >>> fuzzworks.download_fuzzworks_sde_db('sde.db')
        """
        # Get the correct endpoint for the specified db type.
        endpoint = DB_TYPE_TO_FUZZWORKS_ENDPOINT[db_type]

        # Fetch the data from the endpoint.
        try:
            response = self.fetch_data(endpoint)
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to fetch data from Fuzzworks endpoint: {endpoint}.")
            raise e

        # Save the downloaded db to the specified path.
        try:
            with open(db_path, "wb") as db_file:
                db_file.write(response.content)
        except IOError as e:
            logger.error(f"Failed to save Fuzzworks db to path: {db_path}.")
            raise e


if __name__ == "__main__":
    import doctest

    doctest.testmod()
