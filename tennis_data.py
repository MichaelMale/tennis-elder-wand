import pandas as pd
import requests
import datetime
from collections import deque
from io import StringIO

EARLIEST_TOUR_YEAR = 1968


def get_tennis_data(year, tour):
    """
    This function fetches and prepares the tennis match data.

    Args:
        year (int): The year of the tour that you are querying.
        tour (string): The type of tour i.e. WTA or ATP

    Returns:
        DataFrame: The prepared pandas DataFrame.
    """
    tour = tour.lower()
    if tour != "wta" and tour != "atp":
        raise ValueError("Tour value must be either ATP or WTA")

    if year < EARLIEST_TOUR_YEAR or year > datetime.datetime.now().year:
        raise ValueError("Invalid year, year is either before the start of data, or in the future.")

    df = pd.DataFrame()
    tour = tour.lower()
    url = f'https://raw.githubusercontent.com/JeffSackmann/tennis_{tour}/master/{tour}_matches_{year}.csv'
    response = requests.get(url)
    csv_file = StringIO(response.content.decode('utf-8'))

    year_df = pd.read_csv(csv_file)

    # Select only the desired columns
    year_df = year_df[['tourney_name', 'tourney_date', 'winner_name', 'loser_name', 'score', 'round', 'match_num']]

    # Append the yearly data to the main DataFrame
    df = pd.concat([df, year_df])

    # Sort dataframe by date
    df = df.sort_values('tourney_date')

    return df


def find_transfers(data_frame, holder, wand):
    """
    This function iterates over the data frame and finds transfers of the "Elder Wand".

    Args:
        data_frame (DataFrame): The DataFrame to process.
        holder (str): The current holder of the "Elder Wand".
        wand (deque): The deque to store the transfer history.

    Returns:
        None
    """
    for _, row in data_frame.iterrows():
        if row['loser_name'] == holder:
            wand.append(row.tolist())
            holder = row['winner_name']
        if data_frame[(data_frame['loser_name'] == holder)].empty:
            next_loss = data_frame[data_frame['winner_name'] == holder].iloc[0]
            find_transfers(data_frame[data_frame['tourney_date'] > next_loss['tourney_date']], next_loss['loser_name'],
                           wand)
            break


def run_elder_wand_process(year_range):
    for year in year_range:
        df = get_tennis_data(year, 'wta')
        initial_holder = df.iloc[0]['winner_name']

        elder_wand = deque()
        elder_wand.append(df.iloc[0].tolist())  # add the first match data

        find_transfers(df, initial_holder, elder_wand)

        print('The holder of the elder wand is', elder_wand[-1][2], 'in', year)


if __name__ == '__main__':
    run_elder_wand_process(range(2016, 2023 + 1))
