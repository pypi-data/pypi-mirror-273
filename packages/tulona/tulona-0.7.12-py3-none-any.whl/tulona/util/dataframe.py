import logging
from typing import List, Tuple, Union

import pandas as pd

from tulona.exceptions import TulonaFundamentalError

log = logging.getLogger(__name__)


def apply_column_exclusion(
    df: pd.DataFrame,
    primary_key: Union[List, Tuple, str],
    exclude_columns: list,
    ds_name: str,
) -> Union[pd.DataFrame, None]:
    for k in primary_key:
        if k in exclude_columns:
            raise TulonaFundamentalError(
                f"Cannot exclude primary key/join key {k} from comparison"
            )

    missing_cols = []
    for col in exclude_columns:
        if col not in df.columns.tolist():
            missing_cols.append(col)

    if len(missing_cols) > 0:
        log.warning(f"Columns {missing_cols} to be excluded are not present in {ds_name}")
        exclude_columns = list(set(exclude_columns) - set(missing_cols))

    if len(exclude_columns):
        df = df.drop(columns=exclude_columns)
    return df
