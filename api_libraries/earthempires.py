import requests
import os
import pandas as pd
import io

apicode = os.environ.get("apicode")


def get_rank_from_server(server_id):
    response = requests.get(
        f"http://www.earthempires.com/ranks_feed?apicode={apicode}&serverid={server_id}&style=2"
    )
    # Standard output for a country:
    # 22,5004,551,36,slip,53369,21053233,xNAx,F,0,0,0,1,0,0
    return response


def get_govt_from_ranks(ranks):
    data = io.StringIO(ranks.text)
    df = pd.read_csv(data, header=None)
    gov_counts = df[8].value_counts()
    gov_identifier_count = pd.DataFrame(gov_counts).reset_index()
    gov_identifier_count.columns = ["Gov", "Quantity"]
    gov_identifier_count = gov_identifier_count.to_string(index=False)
    return gov_identifier_count


def get_land_from_ranks(ranks):
    # Load the data into a DataFrame
    data = io.StringIO(ranks.text)
    df = pd.read_csv(data, header=None)

    # Select the specified columns: 4, 5, 6, 8, 9 (0-indexed in pandas)
    selected_columns = df.iloc[:, [3, 4, 5, 7, 14]]
    # Filter out rows where column 8 is empty or column 15 is 1
    filtered_df = selected_columns[
        (selected_columns[7].notna()) & (selected_columns[14] != 1)
    ]

    # Drop column 15 from the result
    result_df = filtered_df.drop(columns=[14])

    return result_df


def clan_land(df):
    df.columns = ["Number", "Country", "Land", "Clan"]
    total_land_per_clan = df.groupby("Clan")["Land"].sum().reset_index()
    total_land_per_clan_sorted = total_land_per_clan.sort_values(
        by="Land", ascending=False
    )
    return total_land_per_clan_sorted


def player_land(df):
    df.columns = ["Number", "Country", "Land", "Clan"]
    total_land_per_player = df.groupby("Country")["Land"].sum().reset_index()
    total_land_per_player_sorted = total_land_per_player.sort_values(
        by="Land", ascending=False
    )

    return total_land_per_player_sorted


def coop_info():
    server_id = "22"
    round = "2"
    start = "2024-08-01 00:00"
    end = "2024-09-29 23:59"
    return server_id, round, start, end
