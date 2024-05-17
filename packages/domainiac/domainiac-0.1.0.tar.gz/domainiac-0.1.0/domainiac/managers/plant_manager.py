import datamazing.pandas as pdz
import pandas as pd

from .masterdata_manager import MasterdataManager


class PlantManager(MasterdataManager):
    """
    Manager which simplifies the process of getting plants from masterdata.
    """

    def __init__(
        self,
        db: pdz.Database,
        time_interval: pdz.TimeInterval,
        resolution: pd.Timedelta,
    ) -> None:
        self.db = db
        self.time_interval = time_interval
        self.resolution = resolution

    def get_plants(
        self,
        filters: dict = {},
        columns: list = [
            "plant_id",
            "masterdata_gsrn",
            "datahub_gsrn_e18",
            "installed_power_MW",
            "price_area",
            "valid_from_date_utc",
            "valid_to_date_utc",
        ],
    ) -> pd.DataFrame:
        """Gets the plants for a given plant type.
        Filters for plants valid at the end of time interval.
        Filters by default for plants in operation.
        """
        return self.get_data("masterdataPlant", filters=filters, columns=columns)
