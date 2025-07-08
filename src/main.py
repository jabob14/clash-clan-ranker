import os
import coc
import asyncio
import questionary
import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv
from filehandler import write_to_file, read_from_file
from clandata import update_data

console = Console()

load_dotenv()
COC_EMAIL = os.getenv("COC_EMAIL")
COC_PASSWORD = os.getenv("COC_PASSWORD")
CLAN_TAG = os.getenv("CLAN_TAG")


def main_menu():
    clan_data = read_from_file()
    clan_name = clan_data['clanInfo']['name']

    welcome_panel = Panel(
        f"Welcome to the Clash Ranker for [bold blue]{clan_name}[/bold blue]!",
        title="[bold green]Main Menu[/bold green]",
        border_style="green"
    )
    console.print(welcome_panel)

    choice = questionary.select(
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
    return choice

def view_clan_ranking():
    clan_data = read_from_file()
    member_data = clan_data['memberInfo']

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Rank", style="dim", width=6)
    table.add_column("Name", style="cyan")
    table.add_column("donations", justify="right")
    table.add_column("clanGamesScore", justify="right")
    table.add_column("clanWarLeagueStars", justify="right")
    table.add_column("capitalAttacks", justify="right")
    table.add_column("totalScore", justify="right")

    i = 0
    for member in member_data:
        i += 1
        table.add_row(
            f"{i}",
            f"{member_data[member]['name']}",
            f"{member_data[member]['donations']}",
            f"{member_data[member]['clanGamesScore']}",
            f"{member_data[member]['clanWarLeagueStars']}",
            f"{member_data[member]['capitalAttacks']}",
            f"{member_data[member]['totalScore']}"
        )
    console.print(table)
    questionary.press_any_key_to_continue("Press any key to return to the menu...").ask()


def update_data_from_api():
    console.print("[bold cyan]Updating data from API...[/bold cyan]")
    asyncio.run(update_data(COC_EMAIL, COC_PASSWORD, CLAN_TAG))
    time.sleep(2)
    console.print("[bold green]Data updated successfully![/bold green]")
    time.sleep(4)

def reset_score_menu():
    awnser = questionary.confirm("Are you sure you want to reset the scores?").ask()
    if awnser:
        console.print("[bold cyan]Reseting the scores...[/bold cyan]")
        time.sleep(2)
        console.print("[bold green]Scores have been reset![/bold green]")
        time.sleep(2)
    

if __name__ == "__main__":
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        user_choice = main_menu()
        if user_choice == "View clan ranking":
            view_clan_ranking()

        elif user_choice == "Update clan data":
            update_data_from_api()

        elif user_choice == "Update clan game score":
            pass

        elif user_choice == "Update clan war league stars":
            pass

        elif user_choice == "Update capital raid score":
            pass

        elif user_choice == "Reset scores":
            reset_score_menu()

        elif user_choice == "Exit":
            break

    console.print("[bold yellow]Goodbye![/bold yellow]")