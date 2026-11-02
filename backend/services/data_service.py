import pandas as pd


class DataService:
    def __init__(self, path) -> None:
        self.frame = pd.read_csv(path)

    def values(self, column: str) -> list[str]:
        return sorted(self.frame[column].dropna().astype(str).unique().tolist())

    def years(self) -> list[int]:
        return sorted(self.frame["Year"].dropna().astype(int).unique().tolist())

    def districts(self, state: str | None = None) -> list[str]:
        frame = self.frame if state is None else self.frame[self.frame["State"] == state]
        return sorted(frame["District"].dropna().astype(str).unique().tolist())

    def analytics(self, prediction_count: int) -> dict:
        def grouped(column: str, limit: int | None = None) -> list[dict]:
            values = (
                self.frame.groupby(column, as_index=False)["Yield"]
                .agg(mean="mean", records="size")
                .sort_values("mean", ascending=False)
            )
            if limit:
                values = values.head(limit)
            return [
                {
                    column.lower().replace(" ", "_"): str(row[column]),
                    "mean_yield": float(row["mean"]),
                    "records": int(row["records"]),
                }
                for _, row in values.iterrows()
            ]

        yearly = (
            self.frame.groupby("Year", as_index=False)["Yield"]
            .agg(mean="mean", records="size")
            .sort_values("Year")
        )
        return {
            "dataset": {
                "records": int(len(self.frame)),
                "columns": int(len(self.frame.columns)),
                "year_range": [
                    int(self.frame["Year"].min()),
                    int(self.frame["Year"].max()),
                ],
                "yield": {
                    "min": float(self.frame["Yield"].min()),
                    "max": float(self.frame["Yield"].max()),
                    "mean": float(self.frame["Yield"].mean()),
                    "median": float(self.frame["Yield"].median()),
                },
            },
            "predictions_saved": prediction_count,
            "yield_unit": "Unknown; not specified by the dataset documentation.",
            "by_crop": grouped("Crop"),
            "by_state": grouped("State", 20),
            "by_season": grouped("Season"),
            "by_year": [
                {
                    "year": int(row["Year"]),
                    "mean_yield": float(row["mean"]),
                    "records": int(row["records"]),
                }
                for _, row in yearly.iterrows()
            ],
        }
