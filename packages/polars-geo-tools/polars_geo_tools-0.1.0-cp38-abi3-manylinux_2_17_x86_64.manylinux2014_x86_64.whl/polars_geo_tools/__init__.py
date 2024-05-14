from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Protocol, cast

import polars as pl
from pyogrio.raw import read_arrow

from polars_geo_tools.s2 import *
from polars_geo_tools.utils import (parse_into_expr, parse_version,
                                    register_plugin)

if TYPE_CHECKING:
    from polars.type_aliases import IntoExpr

if parse_version(pl.__version__) < parse_version("0.20.16"):
    from polars.utils.udfs import _get_shared_lib_location

    lib: str | Path = _get_shared_lib_location(__file__)
else:
    lib = Path(__file__).parent

print("lib = {lib}")

# def read_file(filename: str) -> pl.DataFrame:
#     _, table = read_arrow(filename)
#     df = pl.from_arrow(table)
#     return df


# def area(geo_col: IntoExpr) -> pl.Expr:
#     geo_col = parse_into_expr(geo_col)
#     return register_plugin(
#         args=[geo_col],
#         symbol="area",
#         is_elementwise=True,
#         lib=lib,
#     )


# def geom_type(geo_col: IntoExpr) -> pl.Expr:
#     geo_col = parse_into_expr(geo_col)
#     return register_plugin(
#         args=[geo_col],
#         symbol="geom_type",
#         is_elementwise=True,
#         lib=lib,
#     )


def bounds(geo_col: IntoExpr) -> pl.Expr:
    geo_col = parse_into_expr(geo_col)
    return register_plugin(
        args=[geo_col],
        symbol="bounds",
        is_elementwise=True,
        lib=lib,
    )

def lat_lon_to_cell_id(expr: pl.Expr, *, level: int = 30) -> pl.Expr:
    return register_plugin(
        args=[expr],
        symbol="lat_lon_to_cell_id",
        is_elementwise=True,
        lib=lib,
        kwargs={
            "level": level,
        },
    )

def cell_id_to_lat_lon(expr: pl.Expr) -> pl.Expr:
    return register_plugin(
        args=[expr],
        symbol="cell_id_to_lat_lon",
        is_elementwise=True,
        lib=lib,
    )

# class CoordUtilsExpr(pl.Expr):
#     @property
#     def s2(self) -> S2NameSpace:
#         return S2NameSpace(self)
    

# class CTColumn(Protocol):
#     def __cal__(
#         self,
#         name,
#         *more_names,
#     ) -> CoordUtilsExpr:
#         ...

#     def __getattr__(self, name: str) -> pl.Expr:
#         ...

#     @property
#     def s2(self) -> S2NameSpace:
#         ...


# col = cast(CTColumn, pl.col)

# __all__ = ["col"]