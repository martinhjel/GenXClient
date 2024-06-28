from pathlib import Path

import pandas as pd


class DemandData:
    def __init__(
        self, voll: float, demand_segments: pd.DataFrame, rep_periods: pd.DataFrame, time_series: pd.DataFrame
    ) -> None:
        self.voll = voll
        self.demand_segments = demand_segments
        self.rep_periods = rep_periods
        self.time_series = time_series

    @staticmethod
    def from_csv(csv_file_path: Path):
        # Read the CSV file
        df = pd.read_csv(csv_file_path)

        df.loc["Demand_Segment"] = df["Demand_Segment"].astype(int)

        # Extracting data for different parts
        demand_segments_df = (
            df[["Demand_Segment", "Cost_of_Demand_Curtailment_per_MW", "Max_Demand_Curtailment", "$/MWh"]]
            .dropna()
            .reset_index(drop=True)
        )

        rep_periods_df = df[["Rep_Periods", "Timesteps_per_Rep_Period", "Sub_Weights"]].dropna().reset_index(drop=True)
        time_series_df = df[["Time_Index", "Demand_MW_z1", "Demand_MW_z2", "Demand_MW_z3"]]

        # Creating the FullDataset instance
        demand_data = DemandData(
            voll=df["Voll"].dropna().values[0],
            demand_segments=demand_segments_df,
            rep_periods=rep_periods_df,
            time_series=time_series_df,
        )

        return demand_data

    def to_csv(self, csv_file_path: Path):
        combined_df = pd.concat(
            [pd.DataFrame([self.voll], columns=["Voll"]), self.demand_segments, self.rep_periods, self.time_series],
            axis=1,
        )

        combined_df.to_csv(csv_file_path, index=False)


class FuelsData:
    def __init__(self, time_series: pd.DataFrame) -> None:
        self.time_series = time_series

    @staticmethod
    def from_csv(csv_file_path: Path) -> None:
        time_series_df = pd.read_csv(csv_file_path)
        return FuelsData(time_series=time_series_df)

    def to_csv(self, csv_file_path: Path) -> None:
        self.time_series.to_csv(csv_file_path, index=False)


class GeneratorsVariabilityData:
    def __init__(self, time_series: pd.DataFrame):
        self.time_series = time_series

    @staticmethod
    def from_csv(csv_file_path: Path) -> None:
        time_series_df = pd.read_csv(csv_file_path)
        return FuelsData(time_series=time_series_df)

    def to_csv(self, csv_file_path: Path) -> None:
        self.time_series.to_csv(csv_file_path, index=False)
