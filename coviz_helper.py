import numpy as np
import pandas as pd
import logging


DOUBLING_TEMPLATE = "Over this time period, cases doubled roughly every {rate} days."


def load_data(src, use_cached=False, update_cache=False):
    if use_cached:
        df = pd.read_csv(f"data/{src}")
    else:
        try:
            df = pd.read_csv(
                f"https://raw.githubusercontent.com/nytimes/covid-19-data/master/{src}"
            )
        except:
            logging.getLogger("coviz").warning(
                "Unable to fetch latest NY times data, falling back to stale data."
            )
            df = pd.read_csv(f"data/{src}")

        if update_cache:
            df.to_csv(f"data/{src}", index=False)


    # Filter out days with too few cases
    return df[df.cases >= 10]


def process_data(df):
    dates = list(df.date)
    x = np.array(list(range(len(dates))))
    y = list(df.cases)

    a, b = np.polyfit(x, np.log(y), 1)
    y_fit = np.exp(a * x + b)
    return dates, y, y_fit


def construct_doubling_text(start, end, n):
    num_doubles = np.log(start / end) / np.log(2)
    rate = (n - 1) / num_doubles if num_doubles > 0 else float("inf")
    return DOUBLING_TEMPLATE.format(rate=f"{rate:0.1f}")
