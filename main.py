from api_libraries import discord, earthempires
from prettytable import PrettyTable
import datetime


def announce_game_info(round, start_date_str, end_date_str):
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d %H:%M")
    current_date = datetime.datetime.utcnow()

    total_days = (end_date - start_date).total_seconds() / (24 * 60 * 60)
    total_turns = total_days * 24 * 60 // 25

    days_passed = (current_date - start_date).total_seconds() / (24 * 60 * 60)
    days_left = total_days - days_passed

    turns_left = total_turns - (days_passed * 24 * 60 // 25)

    start_date_fmt = start_date.strftime("%b %d %H:%M")
    end_date_fmt = end_date.strftime("%b %d %H:%M")

    announcement = (
        f"```Round {round} {start_date_fmt} - {end_date_fmt}\n"
        f"There are {days_left:.1f} days left\n"
        f"Approximately {turns_left:.0f} turns left to give.```"
    )
    return announcement


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
    # Get server info.
    server_id, round, start, end = earthempires.coop_info()
    announce = announce_game_info(round, start, end)
    discord.msg_discord_stats(announce, "Cooperation Server")

    # Get server ranks.
    ranks = earthempires.get_rank_from_server(server_id)

    # Get government stats.
    gov_stats = earthempires.get_govt_from_ranks(ranks)
    formatted_table_with_title = f"```{gov_stats}```"
    discord.msg_discord_stats(formatted_table_with_title, "Government Totals")

    # Get land stats.
    land_table = earthempires.get_land_from_ranks(ranks)

    # Get clan land stats.
    clan_land_stats = earthempires.clan_land(land_table)
    clan_land_stats = clan_land_stats.head(10)
    clan_land_table = build_clan_table(clan_land_stats)
    formatted_data = clan_land_table.get_string()
    formatted_table_with_title = f"```{formatted_data}```"
    discord.msg_discord_stats(formatted_table_with_title, "top 10 clans | land")

    # Get country land stats.
    country_land_stats = earthempires.player_land(land_table)
    country_land_stats = country_land_stats.head(10)
    country_land_table = build_country_table(country_land_stats)
    formatted_data_countries = country_land_table.get_string()
    formatted_table_with_title_players = f"```{formatted_data_countries}```"
    discord.msg_discord_stats(
        formatted_table_with_title_players, "top 10 countries | land"
    )


if __name__ == "__main__":
    main()
