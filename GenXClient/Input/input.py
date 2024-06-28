# %%
"""
1_three_zones example system
resources:
 - policy_assignments:
    - Resource_minimum_capacity_requirement.csv
 - Storage.csv
 - Thermal.csv
 - Vre.csv
system:
 - Demand_data.csv
 - Fuels_data.csv
 - Generators_variability.csv
 - Network.csv
settings:
 - clp_settings.yml
 - cplex_settings.yml
 - gurobi_settings.yml
 - genx_settings.yml
 - highs_settings.yml
 - time_domain_reduction_settings.yml
policies:
 - CO2_cap.csv
 - Minimum_capacity_requirement.csv
"""

from pathlib import Path

import pandas as pd

from GenXClient.Input.data_models import (
    DemandData,
    FuelsData,
    GeneratorsVariabilityData,
)

directories = {
    "resources": [
        "Storage.csv",
        "Thermal.csv",
        "Vre.csv",
    ],
    "resources/policy_assignments": ["Resource_minimum_capacity_requirement.csv"],
    "system": ["Demand_data.csv", "Fuels_data.csv", "Generators_variability.csv", "Network.csv"],
    "settings": [
        "clp_settings.yml",
        "cplex_settings.yml",
        "gurobi_settings.yml",
        "genx_settings.yml",
        "highs_settings.yml",
        "time_domain_reduction_settings.yml",
    ],
    "policies": ["CO2_cap.csv", "Minimum_capacity_requirement.csv"],
}


class InputClient:
    def __init__(self, case_system: Path) -> None:
        self.case_system = case_system

    @staticmethod
    def create_dataset_structure(self, case_system: Path) -> None:
        """
        Method to create files and folders for dataset
        """

        exist_ok = True  # NB!

        case_system.mkdir(parents=True, exist_ok=exist_ok)

        for folder, files in directories.items():
            folder_path = case_system / folder
            folder_path.mkdir(parents=True, exist_ok=exist_ok)
            for file in files:
                file_path = folder_path / file
                file_path.touch(exist_ok=exist_ok)

    def get_fuels_data(self) -> FuelsData:
        csv_file_path = self.case_system / "system/Fuels_data.csv"
        return FuelsData.from_csv(csv_file_path)

    def set_fuels_data(self, fuels_data: FuelsData) -> None:
        fuels_data.to_csv(self.case_system / "system/Fuels_data.csv")

    def get_demand_data(self) -> DemandData:
        csv_file_path = self.case_system / "system/Demand_data.csv"
        return DemandData.from_csv(csv_file_path)

    def set_demand_data(self, demand_data: DemandData) -> None:
        demand_data.to_csv(self.case_system / "system/Demand_data.csv")

    def get_generator_variability(self) -> GeneratorsVariabilityData:
        csv_file_path = self.case_system / "system/Generators_variability.csv"
        return GeneratorsVariabilityData.from_csv(csv_file_path)

    def set_generator_variability(self, generator_variability_data: GeneratorsVariabilityData) -> None:
        generator_variability_data.to_csv(self.case_system / "system/Generators_variability.csv")


# %%
if __name__ == "__main__":
    # %%

    case_system = Path.cwd() / "Dataset"

    case_system = Path.cwd() / "../GenX/Example_Systems/1_three_zones"

    file = case_system / "system/Fuels_data.csv"
    pd.read_csv(file, index_col=0)

    file = case_system / "system/Demand_data.csv"
    pd.read_csv(file)

    # %%
    case_system = Path.cwd() / "../GenX/Example_Systems/1_three_zones"
    input_client = InputClient(case_system=case_system)

    # %%
    demand_data = input_client.get_demand_data()

    demand_data.demand_segments
    demand_data.voll
    demand_data.rep_periods
    demand_data.time_series

    input_client.set_demand_data(demand_data)
    # %%

    fuels_data = input_client.get_fuels_data()
    fuels_data.time_series

    input_client.set_fuels_data(fuels_data)
# %%

    gen_var = input_client.get_generator_variability()
    
    gen_var.time_series
    
    input_client.set_generator_variability(gen_var)
    
    