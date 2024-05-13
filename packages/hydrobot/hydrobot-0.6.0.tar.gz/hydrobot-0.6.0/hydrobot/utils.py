"""General utilities."""

import numpy as np
import pandas as pd

MOWSECS_OFFSET = 946771200


def mowsecs_to_timestamp(mowsecs):
    """
    Convert MOWSECS (Ministry of Works Seconds) index to datetime index.

    Parameters
    ----------
    index : pd.Index
        The input index in MOWSECS format.

    Returns
    -------
    pd.DatetimeIndex
        The converted datetime index.

    Notes
    -----
    This function takes an index representing time in Ministry of Works Seconds
    (MOWSECS) format and converts it to a pandas DatetimeIndex.

    Examples
    --------
    >>> mowsecs_index = pd.Index([0, 1440, 2880], name="Time")
    >>> converted_index = mowsecs_to_datetime_index(mowsecs_index)
    >>> isinstance(converted_index, pd.DatetimeIndex)
    True
    """
    try:
        mowsec_time = int(mowsecs)
    except ValueError as e:
        raise TypeError("Expected something that is parseable as an integer") from e

    unix_time = mowsec_time - MOWSECS_OFFSET
    timestamp = pd.Timestamp(unix_time, unit="s")
    return timestamp


def timestamp_to_mowsecs(timestamp):
    """
    Convert MOWSECS (Ministry of Works Seconds) index to datetime index.

    Parameters
    ----------
    index : pd.Index
        The input index in MOWSECS format.

    Returns
    -------
    pd.DatetimeIndex
        The converted datetime index.

    Notes
    -----
    This function takes an index representing time in Ministry of Works Seconds
    (MOWSECS) format and converts it to a pandas DatetimeIndex.

    Examples
    --------
    >>> mowsecs_index = pd.Index([0, 1440, 2880], name="Time")
    >>> converted_index = mowsecs_to_datetime_index(mowsecs_index)
    >>> isinstance(converted_index, pd.DatetimeIndex)
    True
    """
    try:
        timestamp = pd.Timestamp(timestamp)
    except ValueError as e:
        raise TypeError("Expected something that is parseable as an integer") from e

    return int((timestamp.timestamp()) + MOWSECS_OFFSET)


def mowsecs_to_datetime_index(index):
    """
    Convert MOWSECS (Ministry of Works Seconds) index to datetime index.

    Parameters
    ----------
    index : pd.Index
        The input index in MOWSECS format.

    Returns
    -------
    pd.DatetimeIndex
        The converted datetime index.

    Notes
    -----
    This function takes an index representing time in Ministry of Works Seconds
    (MOWSECS) format and converts it to a pandas DatetimeIndex.

    Examples
    --------
    >>> mowsecs_index = pd.Index([0, 1440, 2880], name="Time")
    >>> converted_index = mowsecs_to_datetime_index(mowsecs_index)
    >>> isinstance(converted_index, pd.DatetimeIndex)
    True
    """
    try:
        mowsec_time = index.astype(np.int64)
    except ValueError as e:
        raise TypeError("These don't look like mowsecs. Expecting an integer.") from e
    unix_time = mowsec_time.map(lambda x: x - MOWSECS_OFFSET)
    timestamps = unix_time.map(
        lambda x: pd.Timestamp(x, unit="s") if x is not None else None
    )
    datetime_index = pd.to_datetime(timestamps)
    return datetime_index


def datetime_index_to_mowsecs(index):
    """
    Convert datetime index to MOWSECS (Ministry of Works Seconds).

    Parameters
    ----------
    index : pd.DatetimeIndex
        The input datetime index.

    Returns
    -------
    pd.Index
        The converted MOWSECS index.

    Notes
    -----
    This function takes a pandas DatetimeIndex and converts it to an index
    representing time in Ministry of Works Seconds (MOWSECS) format.

    Examples
    --------
    >>> datetime_index = pd.date_range("2023-01-01", periods=3, freq="D")
    >>> mowsecs_index = datetime_index_to_mowsecs(datetime_index)
    >>> isinstance(mowsecs_index, pd.Index)
    True
    """
    return (index.astype(np.int64) // 10**9) + MOWSECS_OFFSET


def merge_series(series_a, series_b, tolerance=1e-09):
    """
    Combine two series which contain partial elements of the same dataset.

    For series 1:a, 2:b and series 1:a, 3:c, will give 1:a, 2:b, 3:c

    Will give an error if series contains contradicting data

    If difference in data is smaller than tolerance, the values of the first series are used

    Parameters
    ----------
    series_a : pd.Series
        One series to combine (preferred when differences are below tolerance)
    series_b : pd.Series
        Second series to combine (overwritten when differences are below tolerance)
    tolerance : numeric
        Maximum allowed difference between the two series for the same timestamp

    Returns
    -------
    pd.Series
        Combined series
    """
    combined = series_a.combine_first(series_b)
    diff = abs(series_b.combine_first(series_a) - combined)
    if max(diff) > tolerance:
        raise ValueError
    else:
        return combined


def change_blocks(raw_series, changed_series):
    """Find all changes between two series."""
    changed_block_list = []
    start_index = None

    raw_iter = iter(raw_series.items())
    changed_iter = iter(changed_series.items())
    raw_next = next(raw_iter, None)
    changed_next = next(changed_iter, None)

    while raw_next is not None or changed_next is not None:
        raw_date, raw_val = raw_next if raw_next else (None, None)
        changed_date, changed_val = changed_next if changed_next else (None, None)

        if raw_date != changed_date:
            # If one series has a timestamp that the other doesn't, treat it as a change
            # Change block goes from the raw timestamp that is missing in the edit to the
            # next value in the edit, i.e the entire gap.
            if start_index is None:
                start_index = raw_date
        elif raw_val != changed_val:
            # If the values at the same timestamp are different, treat it as a change
            if start_index is None:
                # Start of a changed block
                start_index = raw_date
        else:
            if start_index is not None:
                # End of a changed block
                changed_block_list.append((start_index, raw_date))
                start_index = None

        # Move to the next timestamp in each series
        if raw_date == changed_date:
            raw_next = next(raw_iter, None)
            changed_next = next(changed_iter, None)
        elif (raw_date is None) or raw_date < changed_date:
            raw_next = next(raw_iter, None)
        else:
            changed_next = next(changed_iter, None)

    if start_index is not None:
        changed_block_list.append((start_index, raw_series.index[-1]))

    return changed_block_list


def merge_all_comments(hill_checks, pwq_checks, s123_checks, ncrs):
    """Merge all comments coming in from various sources.

    Sorry, not sure where to put this.
    """
    hill_checks = hill_checks.rename(columns={"Water Temperature Check": "Temp Check"})
    hill_checks = hill_checks.reset_index()
    pwq_checks = pwq_checks.reset_index()
    s123_checks = s123_checks.reset_index()
    ncrs = ncrs.reset_index()

    hill_checks["Source"] = "Hilltop Check Data"
    pwq_checks["Source"] = "Provisional Water Quality"
    s123_checks["Source"] = "Survey123 Inspections"
    ncrs["Source"] = "Non-conformance Reports"

    all_comments = pd.concat(
        [
            hill_checks[["Time", "Comment", "Source"]],
            pwq_checks[["Time", "Comment", "Source"]],
            s123_checks[["Time", "Comment", "Source"]],
            ncrs[["Time", "Comment", "Source"]],
        ],
        ignore_index=True,
        sort=False,
    )
    all_comments = all_comments.dropna(axis=1, how="all")

    all_comments["Time"] = all_comments["Time"].dt.strftime("%Y-%m-%d %H:%M:%S")

    all_comments = all_comments.sort_values(by="Time")

    return all_comments
