from configparser import ConfigParser
from typing import Optional

from pystratum_backend.ConstantWorker import ConstantWorker
from pystratum_backend.RoutineLoaderWorker import RoutineLoaderWorker
from pystratum_backend.RoutineWrapperGeneratorWorker import RoutineWrapperGeneratorWorker
from pystratum_backend.StratumIO import StratumIO


class Backend:
    """
    Semi interface for PyStratum's backends.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def create_constant_worker(self, settings: ConfigParser, io: StratumIO) -> Optional[ConstantWorker]:
        """
        Creates the object that does the actual execution of the constant command for the backend.

        :param settings: The settings from the PyStratum configuration file.
        :param io: The output object.
        """
        return None

    # ------------------------------------------------------------------------------------------------------------------
    def create_routine_loader_worker(self, settings: ConfigParser, io: StratumIO) -> Optional[RoutineLoaderWorker]:
        """
        Creates the object that does the actual execution of the routine loader command for the backend.

        :param settings: The settings from the PyStratum configuration file.
        :param io: The output object.
        """
        return None

    # ------------------------------------------------------------------------------------------------------------------
    def create_routine_wrapper_generator_worker(self, settings: ConfigParser, io: StratumIO) -> Optional[
        RoutineWrapperGeneratorWorker]:
        """
        Creates the object that does the actual execution of the routine wrapper generator command for the backend.

        :param settings: The settings from the PyStratum configuration file.
        :param io: The output object.
        """
        return None

# ----------------------------------------------------------------------------------------------------------------------
