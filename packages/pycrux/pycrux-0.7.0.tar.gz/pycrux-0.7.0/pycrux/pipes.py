import polars as pl


def drop_row_that_is_all_null(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(~pl.all_horizontal(pl.all().is_null()))
