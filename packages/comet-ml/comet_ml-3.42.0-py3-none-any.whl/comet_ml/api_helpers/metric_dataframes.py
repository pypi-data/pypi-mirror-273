# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2021 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************

import logging
from typing import TYPE_CHECKING, Any, Dict, List

if TYPE_CHECKING:
    import pandas as pd

LOGGER = logging.getLogger(__name__)


def get_dataframe_from_multi_metrics(
    multi_metrics: Dict, x_axis: str, columns: List
) -> "pd.DataFrame":
    import numpy as np
    import pandas as pd

    data = []
    keys = ["experiment_key", x_axis]

    for experiment in multi_metrics.values():
        experiment_key = experiment.get("experimentKey", "")
        experiment_name = experiment.get("experimentName", "")
        experiment_metrics = experiment.get("metrics", [])

        for metric in experiment_metrics:
            metric_name = metric.get("metricName", "")

            if metric_name not in columns:
                continue

            metric_values = metric.get("values", [])
            metric_x_axis = metric.get(x_axis + "s", [])
            metric_x_axis_range = _get_x_axis_range(x_axis, metric_x_axis)

            for x_axis_value in metric_x_axis_range:
                if x_axis_value not in metric_x_axis:
                    metric_value = np.nan
                else:
                    metric_value_idx = metric_x_axis.index(x_axis_value)
                    metric_value = _parse_value(metric_values[metric_value_idx])

                data.append(
                    {
                        "experiment_key": experiment_key,
                        "experiment_name": experiment_name,
                        metric_name: metric_value,
                        x_axis: x_axis_value,
                    }
                )

    df = pd.DataFrame(data, columns=columns)

    if df.empty:
        return df[columns]

    df = df[columns].groupby(keys).aggregate("last").reset_index()

    return df[columns]


def interpolate_metric_dataframe(
    df: "pd.DataFrame", x_axis: str, columns: List
) -> "pd.DataFrame":
    NUMERICS = ["int16", "int32", "int64", "float16", "float32", "float64"]
    numeric_columns_to_interpolate = df.select_dtypes(include=NUMERICS).columns.tolist()

    if x_axis in numeric_columns_to_interpolate:
        numeric_columns_to_interpolate.remove(x_axis)

    experiment_keys = df["experiment_key"].unique()

    for experiment_key in experiment_keys:
        mask = (
            df["experiment_key"] == experiment_key,
            numeric_columns_to_interpolate,
        )
        df.loc[mask] = df.loc[mask].interpolate(
            method="linear", limit_direction="both", limit_area="inside"
        )

    return df[columns]


def _parse_value(element: Any) -> Any:
    try:
        if element is None:
            return None
        return float(element)
    except ValueError:
        return element


def _get_x_axis_range(x_axis: str, x_axis_values: List) -> List:
    filtered_x_axis_values = [x for x in x_axis_values if x is not None]

    if len(filtered_x_axis_values) == 0:
        return []

    if x_axis == "duration":
        import numpy as np

        return list(
            np.linspace(
                min(filtered_x_axis_values), max(filtered_x_axis_values), num=100
            )
        )

    return list(range(filtered_x_axis_values[0], filtered_x_axis_values[-1] + 1))
