from typing import Any, List

import pandas as pd
from pandas.core.groupby import DataFrameGroupBy

"""
Functions meant to check the content, values or attributes of a data object.
"""


def is_grouped(dataframe: pd.DataFrame) -> bool:
    """Check if the data argument is grouped."""
    return isinstance(dataframe, DataFrameGroupBy)


def get_groups(dataframe: pd.DataFrame) -> List[Any]:
    """
    If grouped, then return [column_name(s)] ELSE [None].
    Returns list(str).
    """
    if is_grouped(dataframe):
        group_vars = dataframe.keys
        if isinstance(group_vars, str):
            group_vars = [group_vars]
        return group_vars
    else:
        return [None]


def return_data(
    dataframe: pd.DataFrame = pd.DataFrame(None),
) -> pd.DataFrame:
    """return dataframe from grouped or standard DataFrame"""
    if is_grouped(dataframe):
        return dataframe.obj.reset_index()
    else:
        return dataframe


def add_groups_to_combos(
    group_vars: list[str], combos: list[list[str]]
) -> List[List[Any]]:
    """adds a fixed list to a list of lists"""
    combos_plus = []
    for combo in combos:
        combo_plus = group_vars + combo
        combos_plus.append(combo_plus)
    return combos_plus


def group_sizes(grouped_df: DataFrameGroupBy) -> pd.DataFrame:
    """
    Get the size of each group from a grouped Pandas DataFrame.

    Parameters:
    - grouped_df: The grouped Pandas DataFrame.

    Returns:
    - A DataFrame containing the size of each group.
    """
    temp = pd.DataFrame(grouped_df.size()).reset_index()
    results_df = temp.rename(columns={0: "n_rows"})

    return results_df
