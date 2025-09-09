import os
import asyncio
import questionary
import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv
from filehandler import write_to_file, read_from_file
from clandata import update_data
from scorelogic import update_score, sort_members_by_score, reset_scores
from config import *

load_dotenv()
console = Console()


def view_clan_ranking(clan_data):
    WIDTH = 10
    member_data = clan_data['memberInfo']
    total_members = clan_data['clanInfo']['members']
    avg_score = sum(member_data[member]['totalScore'] for member in member_data) / total_members
    total_score_values[1] = avg_score
    total_score_values[2] = avg_score * 2

    table = Table(
        title = "CLAN RANKING LEADERBOARD",
        title_style = "bold yellow",
        show_header = True,
        header_style = "bold white",
        row_styles = ["", "dim"]
    )

    table.add_column("Rank",        justify = "left",  width = 6,         style = "bold yellow",)
    table.add_column("Name",        justify = "left",  min_width = WIDTH, style = "bold white",)
    table.add_column("Donations",   justify = "right", min_width = WIDTH, style = "bold bright_cyan")
    table.add_column("CG Score",    justify = "right", min_width = WIDTH)
    table.add_column("CWL Stars",   justify = "right", min_width = WIDTH)
    table.add_column("CA W1",       justify = "right", min_width = WIDTH)
    table.add_column("CA W2",       justify = "right", min_width = WIDTH)
    table.add_column("CA W3",       justify = "right", min_width = WIDTH)
    table.add_column("CA W4",       justify = "right", min_width = WIDTH)
    table.add_column("CA W5",       justify = "right", min_width = WIDTH)
    table.add_column("CA Total",    justify = "right", min_width = WIDTH)
    table.add_column("Bonus Score", justify = "right", min_width = WIDTH)
    table.add_column("Total Score", justify = "right", min_width = WIDTH)

    position = 0
    for member in member_data:
        position += 1
        
        # Determine color of the clan game score
        cg_score = member_data[member]['clanGamesScore']
        cg_style = get_color_for_score(cg_score, clan_games_scores_values)
        cg_score_text = f"[{cg_style}]{cg_score}[/]"

        # Determine color of the clan war league stars
        cwl_stars = member_data[member]['clanWarLeagueStars']
        cwl_style = get_color_for_score(cwl_stars, clan_war_league_stars_values)
        cwl_stars_text = f"[{cwl_style}]{cwl_stars}[/]"

        # Determine color of the capital raid score
        capital_raid_score_texts = []
        for week in range(1, 6):
            week_key = f'capitalAttacksWeek{week}'
            week_score = member_data[member][week_key]
            week_style = get_color_for_score(week_score, capital_raid_score_values)
            capital_raid_score_texts.append(f"[{week_style}]{week_score}[/]")

        # Calculate total capital attacks
        member_total_capital_attacks = member_data[member]['capitalAttacks']
        total_capital_attacks_style = get_color_for_score(member_total_capital_attacks, total_capital_attacks_values)
        total_capital_attacks_text = f"[{total_capital_attacks_style}]{member_total_capital_attacks}[/]"


        # Determine color of the bonus score
        bonus_score = member_data[member]['bonusScore']
        bonus_score_style = get_color_for_score(bonus_score, bonus_score_values)
        bonus_score_text = f"[{bonus_score_style}]{bonus_score}[/]"

        # Determine color of the score
        total_score = member_data[member]['totalScore']
        score_style = get_color_for_score(total_score, total_score_values)
        total_score_text = f"[{score_style}]{total_score}[/]"

        table.add_row(
            f"{position}",
            f"{member_data[member]['name']}",
            f"{member_data[member]['donations']}",
            cg_score_text,
            cwl_stars_text,
            capital_raid_score_texts[0],
            capital_raid_score_texts[1],
            capital_raid_score_texts[2],
            capital_raid_score_texts[3],
            capital_raid_score_texts[4],
            total_capital_attacks_text,
            bonus_score_text,
            total_score_text
        )

    console.print(table)
    console.print(f" 📊 [bold]Stats:[/bold] {total_members} members | Average Score: [cyan]{avg_score:.1f}[/cyan]")
    questionary.press_any_key_to_continue("Press any key to return to the menu...").ask()


def get_color_for_score(score, score_type):
    if score >= score_type[-1]:
        return "bold green"
    elif score >= score_type[-2]:
        return "bold yellow"
    elif score > score_type[0]:
        return "bold orange3"
    else:
        return "bold bright_red"


def reset_score_menu(clan_data):
    answer = questionary.confirm("Are you sure you want to reset the scores?").ask()
    if answer:
        member_info = clan_data['memberInfo']
        console.print("[bold cyan]Reseting the scores...[/bold cyan]")
        member_info = reset_scores(member_info)
        time.sleep(1)
        console.print("[bold green]Scores have been reset![/bold green]")
        time.sleep(2)
        clan_data['memberInfo'] = member_info
        write_to_file(clan_data)
        return clan_data
    else:
        console.print("[bold yellow]Reset cancelled.[/bold yellow]")
        time.sleep(2)
        return clan_data


def update_datas(type, clan_data):
    member_list = clan_data['memberInfo']
    member_count = clan_data['clanInfo']['members']
    current_member = 0

    for member in member_list:
        current_member += 1
        current_score = member_list[member][type]
        console.print(f"Updating {type} for [yellow]{member_list[member]['name']}[/yellow] (current: [blue]{current_score}[/blue])")
        new_score = questionary.text(
                f"Enter new score (press Enter to keep current):"
            ).ask()

        if new_score.strip():
            try:
                member_list[member][type] = int(new_score)
                console.print(f"[green]Updated {member_list[member]['name']} score to {new_score}[/green] ")
            except ValueError:
                console.print(f"[red]Invalid input. Keeping current score: {current_score}[/red]")
        else:
            console.print(f"[yellow]Keeping current score: {current_score}[/yellow]")
        console.print(f"[bold blue]Progress: {current_member}/{member_count}[/bold blue]\n")
    
    member_list = update_score(member_list)
    member_list = sort_members_by_score(member_list)

    clan_data['memberInfo'] = member_list
    write_to_file(clan_data)
    return clan_data


def main_menu(COC_EMAIL, COC_PASSWORD, CLAN_TAG):
    clan_data = asyncio.run(update_data(COC_EMAIL, COC_PASSWORD, CLAN_TAG))
    clan_name = clan_data['clanInfo']['name']

    welcome_panel = Panel(
        f"Welcome to the Clash Ranker for [bold blue]{clan_name}[/bold blue]!",
        title="[bold green]Main Menu[/bold green]",
        border_style="green"
    )

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(welcome_panel)
        user_choice = questionary.select(
            "What would you like to do?",
            choices=[
                "View clan ranking",
                "Update clan data",
                "Update clan game score",
                "Update clan war league stars",
                "Update capital raid score",
                "Reset scores",
                "Exit"
            ]
        ).ask()

        if user_choice == "View clan ranking":
            view_clan_ranking(clan_data)

        elif user_choice == "Update clan data":
            clan_data = asyncio.run(update_data(COC_EMAIL, COC_PASSWORD, CLAN_TAG))
            time.sleep(1)
            console.print("[bold green]Data updated successfully![/bold green]")
            time.sleep(2)

        elif user_choice == "Update clan game score":
            clan_data = update_datas("clanGamesScore", clan_data)

        elif user_choice == "Update clan war league stars":
            clan_data = update_datas("clanWarLeagueStars", clan_data)

        elif user_choice == "Update capital raid score":

            # Determine which week to update
            week = questionary.select(
                "What week?",
                choices=list(WEEK_MAPPING.keys())
            ).ask()

            # Get the corresponding week key
            week_to_change = WEEK_MAPPING[week]
            clan_data = update_datas(week_to_change, clan_data)

        elif user_choice == "Reset scores":
            clan_data = reset_score_menu(clan_data)

        elif user_choice == "Exit":
            break


if __name__ == "__main__":
    # Get environment variables
    COC_EMAIL = os.getenv("COC_EMAIL")
    COC_PASSWORD = os.getenv("COC_PASSWORD")
    CLAN_TAG = os.getenv("CLAN_TAG")

     # Check if all variables exist
    if not COC_EMAIL or not COC_PASSWORD or not CLAN_TAG:
        console.print("[bold red]Error: Missing environment variables![/bold red]")
        console.print("Please create a .env file with:")
        console.print("COC_EMAIL = your_email")
        console.print("COC_PASSWORD = your_password")
        console.print("CLAN_TAG = your_clan_tag")
        exit(1)

    # Start the main menu
    main_menu(COC_EMAIL, COC_PASSWORD, CLAN_TAG)