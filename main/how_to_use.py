import utils
import pandas as pd


def main():
    # df with all the main links to be collected
    df = pd.read_csv("spyders_links.csv")

    # runs the utils library that collects spyders and saves it to an external .txt file
    utils.main(df)

if __name__ == "__main__":
    main()