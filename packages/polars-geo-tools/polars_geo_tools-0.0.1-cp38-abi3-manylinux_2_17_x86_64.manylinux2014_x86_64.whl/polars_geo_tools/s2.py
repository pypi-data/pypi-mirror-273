import pathlib

import polars as pl


@pl.api.register_expr_namespace("s2")
class S2NameSpace:
    def __init__(self, expr: pl.Expr):
        self._expr = expr
    

    def lat_lon_to_cell_id(self, level: int = 30) -> pl.Expr:
        if level < 1 or level > 30:
            raise ValueError("`level` parameter must be between 1 and 30!")

        return self._expr.register_plugin(
            plugin_path=pathlib.Path(__file__).parent,
            symbol="lat_lon_to_cell_id",
            is_elementwise=True,
            kwargs={
                "level": level,
            }
        )


