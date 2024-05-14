import abc

from mysql.connector import MySQLConnection


class MySqlConnector:
    """
    Interface for classes for connecting to a MySql instances.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def connect(self) -> MySQLConnection:
        """
        Connects to the MySql instance.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def disconnect(self) -> None:
        """
        Disconnects from the MySql instance.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def is_alive(self) -> bool:
        """
        Returns whether Python is (still) connected to a MySQL or MariaDB instance.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
