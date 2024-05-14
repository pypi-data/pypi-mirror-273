import pathlib

import polars as pl
from polars_geo_tools.utils import (parse_version, register_plugin)

if parse_version(pl.__version__) < parse_version("0.20.16"):
    from polars.utils.udfs import _get_shared_lib_location

    lib: str | pathlib.Path = _get_shared_lib_location(__file__)
else:
    lib = pathlib.Path(__file__).parent


def lat_lon_to_resolution(expr: pl.Expr, *, resolution: int = 15) -> pl.Expr:
    if resolution < 1 or resolution > 15:
        raise ValueError("`resolution` parameter must be integer value from 1 to 15")
    return register_plugin(
        args=[expr],
        symbol="lat_lon_to_resolution",
        is_elementwise=True,
        lib=lib,
        kwargs={
            "resolution": resolution,
        },
    )