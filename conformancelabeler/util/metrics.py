import pandas as pd


def get_activity_count(df: pd.DataFrame, event_name: str, case_id_col='case:concept:name',
                       activity_col="concept:name") -> pd.DataFrame:
    df = df.merge(df.groupby([case_id_col])[activity_col]
                  .value_counts().unstack(fill_value=0
                                          ).loc[:, event_name].reset_index()
                  .rename(columns={event_name: "Count " + event_name}),
                  on=[case_id_col], how="left")
    return df


def get_event_duration(log: pd.DataFrame, case_id_col='case:concept:name',
                       timestamp_col='time:timestamp'):
    log[timestamp_col] = log[timestamp_col].dt.tz_localize(None)
    log["duration"] = (log.groupby(case_id_col)[timestamp_col].diff()).dt.seconds.shift(-1)
    return log


def get_cumulative_duration(log: pd.DataFrame, case_id_col='case:concept:name',
                            timestamp_col='time:timestamp'):
    dur = False
    if not "duration" in log.columns.tolist():
        log = get_event_duration(log, case_id_col=case_id_col, timestamp_col=timestamp_col)
    log["cumulative_duration"] = log.groupby(case_id_col)["duration"].apply(lambda x: x.cumsum())
    if dur:
        log = log.drop(columns=["duration"])
    return log


def get_total_duration(log: pd.DataFrame, case_id_col='case:concept:name',
                       timestamp_col='time:timestamp'):
    dur = False
    if not "duration" in log.columns.tolist():
        log = get_event_duration(log, case_id_col=case_id_col, timestamp_col=timestamp_col)
        dur = True
    log["total_duration"] = log.groupby(case_id_col)["duration"].transform('sum')
    if dur:
        log = log.drop(columns=["duration"])
    return log


def get_time_attributes(log: pd.DataFrame,  timestamp_col='time:timestamp'):
    log["month"] = log[timestamp_col].dt.month
    log["weekday"] = log[timestamp_col].dt.weekday
    log["hour"] = log[timestamp_col].dt.hour
    return log


def get_seq_length(log: pd.DataFrame, case_id_col='case:concept:name'):
    log = log.merge(log.groupby(case_id_col).size().reset_index().rename(columns={0: "l"}),
                    on=[case_id_col], how="left")
    return log

