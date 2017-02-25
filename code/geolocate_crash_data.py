import geocoder
import pandas as pd
import os


def geocode(x):
    """
    Converts a text description of a location to a lat/long
    :param x: text description of a location
    :return: lat/long
    """
    g = geocoder.google(x)
    return g.latlng


def prep_data(x, local_string):
    """
    Appends the city (or county) to the geo_loc string
    """
    x += local_string
    return x



def load_data():
    normal_fn = os.path.join(os.path.dirname(__file__), "../data/derived/normal_il_data.csv" )
    bloomington_fn = os.path.join(os.path.dirname(__file__), "../data/derived/bloomington_il_data.csv" )
    mclean_fn = os.path.join(os.path.dirname(__file__), "../data/derived/mclean_county_data.csv" )

    normal_df = pd.read_csv(normal_fn)
    bloomington_df = pd.read_csv(bloomington_fn)
    mclean_df = pd.read_csv(mclean_fn)
    bike_data = {"normal": normal_df, "bloomington": bloomington_df, "mclean ": mclean_df}
    return bike_data

def write_data(k, v):
    fn = os.path.join(os.path.dirname(__file__), "../data/derived/" + k + "_il_geocoded.csv")
    v.to_csv(fn, index=False)


def main():
    bike_data = load_data()
    for k, v in bike_data.items():
        loc_string = " " + k + ",illinois"
        v['geo_loc'] = v['geo_loc'].apply(prep_data, args=(loc_string,)) # append location string to series
        v['lat_long'] = v['geo_loc'].map(geocode)
        write_data(k, v)


if __name__ == "__main__":
    main()