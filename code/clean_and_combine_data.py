"""
Cleans all three datasets and combines them for future analysis
"""
import os
import pandas as pd


def load_data():
    normal_fn = os.path.join(os.path.dirname(__file__), "../data/derived/normal_il_geocoded.csv" )
    bloomington_fn = os.path.join(os.path.dirname(__file__), "../data/derived/bloomington_il_geocoded.csv" )
    mclean_fn = os.path.join(os.path.dirname(__file__), "../data/derived/mclean _il_geocoded.csv" )

    normal_df = pd.read_csv(normal_fn)
    bloomington_df = pd.read_csv(bloomington_fn)
    mclean_df = pd.read_csv(mclean_fn)
    bike_data = {"normal": normal_df, "bloomington": bloomington_df, "mclean": mclean_df}
    return bike_data


def merge_datasets(bike_data):
    df = pd.DataFrame()
    for k,v in bike_data.items():
        v["data_source"] = k
        df = pd.concat([df, v], axis=0)
    return df


def clean_date(df):
    df['crash_time'] = pd.to_datetime(df.date + " " + df.time)
    df = df.drop(['date', 'time'], axis=1)
    return df


def split_lat_long(x):
    x = x.strip("[,]")
    lat, long = x.split(",")
    return pd.Series({"lat":lat, "long":long})


def clean_lat_long(df):
    df = df.merge(df.lat_long.apply(split_lat_long), left_index=True, right_index=True)
    df = df.drop(['lat_long'], axis=1)
    return df


def write_data(df):
    fn = os.path.join(os.path.dirname(__file__), "../data/derived/complete_dataset.csv")
    v.to_csv(fn, index=False)


def main():
    bike_data = load_data()
    df = merge_datasets(bike_data)
    df = clean_date(df)
    df = clean_lat_long(df)

    print(df.shape)
    print(df.columns)

if __name__ == "__main__":
    main()