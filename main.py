from api_libraries import discord, earthempires
from prettytable import PrettyTable


def abbreviate_text(text, max_length):
    """
    Abbreviates the given text if it exceeds the maximum length.
    """
    if len(text) > max_length:
        return text[: max_length - 2] + ".."
    return text


def build_clan_table(clan_land_stats):
    """
    Builds a PrettyTable object with clan land statistics.
    """
    table = PrettyTable()
    table.border = False
    table.field_names = ["Clan", "Land"]
    table.align["Clan"] = "l"
    table.align["Land"] = "r"
    for _, row in clan_land_stats.iterrows():
        formatted_points = f"{row['Land']:,}"
        table.add_row([row["Clan"], formatted_points])
    return table


def build_country_table(country_land_stats):
    """
    Builds a PrettyTable object with country land statistics.
    """
    table = PrettyTable()
    table.border = False
    table.field_names = ["Country", "Land"]
    table.align["Country"] = "l"
    table.align["Land"] = "r"
    for _, row in country_land_stats.iterrows():
        formatted_points = f"{row['Land']:,}"
        formatted_row = abbreviate_text(row["Country"], 15)
        table.add_row([formatted_row, formatted_points])
    return table


def main():
    """
    Retrieves land data, builds tables, and sends messages to Discord.

    This function retrieves land data from the EE API, builds tables with clan and country land statistics,
    and sends the formatted tables as messages to a Discord channel.
    """
    land_table = earthempires.get_land_from_ranks(
        "22"
    )  # 22 is the server ID for the Cooperation server.

    clan_land_stats = earthempires.clan_land(land_table)
    clan_land_stats = clan_land_stats.head(10)
    clan_land_table = build_clan_table(clan_land_stats)
    formatted_data = clan_land_table.get_string()
    formatted_table_with_title = f"```{formatted_data}```"
    discord.msg_coop_land_feed(formatted_table_with_title, "top 10 clans | land")

    country_land_stats = earthempires.player_land(land_table)
    country_land_stats = country_land_stats.head(10)
    country_land_table = build_country_table(country_land_stats)
    formatted_data_countries = country_land_table.get_string()
    formatted_table_with_title_players = f"```{formatted_data_countries}```"
    discord.msg_coop_land_feed(
        formatted_table_with_title_players, "top 10 countries | land"
    )


if __name__ == "__main__":
    main()