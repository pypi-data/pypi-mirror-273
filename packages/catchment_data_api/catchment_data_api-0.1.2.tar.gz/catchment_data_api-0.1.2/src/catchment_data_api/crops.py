"""
Crops Module
------------

This module contains the Crops class, which is responsible for managing and calculating crop data.
"""

import pandas as pd
from catchment_data_api.catchment_data_api import CatchmentDataAPI
from catchment_data_api.static_data import StaticData

class Crops:
    """
    A class to manage and calculate crop data within a specified catchment area.

    This class utilizes LUCAS (Land Use and Coverage Area frame Survey) data and 
    cultivated land data to derive the area of different crops within a catchment.

    Attributes:
        api (CatchmentDataAPI): An instance of the CatchmentDataAPI for accessing catchment data.
    """
    def __init__(self):
        self.api = CatchmentDataAPI()
        self.static_data = StaticData()


    def _derive_crops(self, catchment):
        """
        Derives crop data for a specified catchment based on LUCAS data and cultivated land data.
        This method calculates the total area for each crop type within the catchment by utilizing
        the proportion of each crop type from LUCAS data and the total cultivated land area.

        Parameters:
            catchment (str): The name of the catchment area.

        Returns:
            pandas.DataFrame: A DataFrame containing the derived crop data for the catchment, including
            the catchment name, crop types, and their respective areas in hectares.
        """
        lucas_df = self.api.get_catchment_lucas_data_by_catchment_name(catchment)
        cultivated_df = self.api.get_catchment_cultivated_data_by_catchment_name(catchment)
        
        # Assume crops are mineral 
        total_cultivated_land_area = cultivated_df['total_hectares'].sum()

        data = []
        
        if lucas_df.empty:
            row = {
                "catchment": self.api.format_catchment_name(catchment),
                "crop": self.static_data.get_default_crop(),
                "area_ha": total_cultivated_land_area
            }
            data.append(row)

            return pd.DataFrame(data)
        
        else:
            for crop in lucas_df['crop_type'].unique():
                # Sum the crop proportions for each crop type
                crop_proportion_sum = lucas_df.loc[lucas_df['crop_type'] == crop]['crop_proportion'].sum()
                row = {
                    "catchment": self.api.format_catchment_name(catchment),
                    "crop": crop,
                    "area_ha": total_cultivated_land_area * crop_proportion_sum
                }
                data.append(row)
  
            return pd.DataFrame(data)
    

    def get_catchment_crops(self, catchment):
        """
        Public method to retrieve the derived crop data for a specified catchment.
        This method serves as an interface to access the calculated crop areas
        and types within the catchment.

        Parameters:
            catchment (str): The name of the catchment area.

        Returns:
            pandas.DataFrame: A DataFrame containing the derived crop data for the specified catchment.
        """
        df = self._derive_crops(catchment)

        return df