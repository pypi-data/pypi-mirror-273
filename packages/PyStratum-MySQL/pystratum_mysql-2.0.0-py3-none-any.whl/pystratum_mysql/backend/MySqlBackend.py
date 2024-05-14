from configparser import ConfigParser
from typing import Optional

from pystratum_backend.Backend import Backend
from pystratum_backend.ConstantWorker import ConstantWorker
from pystratum_backend.RoutineLoaderWorker import RoutineLoaderWorker
from pystratum_backend.RoutineWrapperGeneratorWorker import RoutineWrapperGeneratorWorker
from pystratum_backend.StratumIO import StratumIO

from pystratum_mysql.backend.MySqlConstantWorker import MySqlConstantWorker
from pystratum_mysql.backend.MySqlRoutineLoaderWorker import MySqlRoutineLoaderWorker
from pystratum_mysql.backend.MySqlRoutineWrapperGeneratorWorker import MySqlRoutineWrapperGeneratorWorker


class MySqlBackend(Backend):
    """
    PyStratum Backend for MySQL & MariaDB.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def create_constant_worker(self, config: ConfigParser, io: StratumIO) -> Optional[ConstantWorker]:
        """
        Creates the object that does the actual execution of the constant command for the backend.

        :param config: The settings from the PyStratum configuration file.
        :param io: The output object.
        """
        return MySqlConstantWorker(io, config)

    # ------------------------------------------------------------------------------------------------------------------
    def create_routine_loader_worker(self, config: ConfigParser, io: StratumIO) -> Optional[RoutineLoaderWorker]:
        """
        Creates the object that does the actual execution of the routine loader command for the backend.

        :param config: The settings from the PyStratum configuration file.
        :param io: The output object.
        """
        return MySqlRoutineLoaderWorker(io, config)

    # ------------------------------------------------------------------------------------------------------------------
    def create_routine_wrapper_generator_worker(self, config: ConfigParser, io: StratumIO) \
            -> Optional[RoutineWrapperGeneratorWorker]:
        """
        Creates the object that does the actual execution of the routine wrapper generator command for the backend.

        :param config: The settings from the PyStratum configuration file.
        :param io: The output object.
        """
        return MySqlRoutineWrapperGeneratorWorker(io, config)

# ----------------------------------------------------------------------------------------------------------------------
