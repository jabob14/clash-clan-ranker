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

def view_clan_ranking(clan_data):

    member_data = clan_data['memberInfo']

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Rank", style="dim", width=6)
    table.add_column("Name", style="cyan")
    table.add_column("Donations", justify="right")
    table.add_column("CG Score", justify="right")
    table.add_column("CWL Stars", justify="right")
    table.add_column("CA W1", justify="right")
    table.add_column("CA W2", justify="right")
    table.add_column("CA W3", justify="right")
    table.add_column("CA W4", justify="right")
    table.add_column("CA Total", justify="right")
    table.add_column("Total Score", justify="right")

    i = 0
    for member in member_data:
        i += 1
        table.add_row(
            f"{i}",
            f"{member_data[member]['name']}",
            f"{member_data[member]['donations']}",
            f"{member_data[member]['clanGamesScore']}",
            f"{member_data[member]['clanWarLeagueStars']}",
            f"{member_data[member]['capitalAttacksWeek1']}",
            f"{member_data[member]['capitalAttacksWeek2']}",
            f"{member_data[member]['capitalAttacksWeek3']}",
            f"{member_data[member]['capitalAttacksWeek4']}",
            f"{member_data[member]['capitalAttacks']}",
            f"{member_data[member]['totalScore']}"
        )
    console.print(table)
    questionary.press_any_key_to_continue("Press any key to return to the menu...").ask()


def update_data_from_api():
    console.print("[bold cyan]Updating data from API...[/bold cyan]")
    clan_data = asyncio.run(update_data(COC_EMAIL, COC_PASSWORD, CLAN_TAG))
    time.sleep(2)
    console.print("[bold green]Data updated successfully![/bold green]")
    time.sleep(2)
    return clan_data

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

    for member in member_list:
        current_score = member_list[member][type]
        console.print(f"Updating {type} for [yellow]{member_list[member]['name']}[/yellow] (current: [blue]{current_score}[/blue])")
        new_score = questionary.text(
                f"Enter new score (press Enter to keep current):"
            ).ask()

        if new_score.strip():  # If user entered something
            try:
                member_list[member][type] = int(new_score)
                console.print(f"[green]Updated {member_list[member]['name']} score to {new_score}[/green] \n")
            except ValueError:
                console.print(f"[red]Invalid input. Keeping current score: {current_score}[/red] \n")
        else:
            console.print(f"[yellow]Keeping current score: {current_score}[/yellow] \n")
    
    member_list = update_score(member_list)
    member_list = sort_members_by_score(member_list)

    clan_data['memberInfo'] = member_list
    write_to_file(clan_data)
    return clan_data

if __name__ == "__main__":
    clan_data = asyncio.run(update_data(COC_EMAIL, COC_PASSWORD, CLAN_TAG))
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        user_choice = main_menu()
        if user_choice == "View clan ranking":
            view_clan_ranking(clan_data)

        elif user_choice == "Update clan data":
            clan_data = update_data_from_api()

        elif user_choice == "Update clan game score":
            clan_data = update_datas("clanGamesScore", clan_data)

        elif user_choice == "Update clan war league stars":
            clan_data = update_datas("clanWarLeagueStars", clan_data)

        elif user_choice == "Update capital raid score":
            choice = questionary.select(
                "What week?",
                choices=[
                    "Week 1",
                    "Week 2",
                    "Week 3",
                    "Week 4"
                ]
            ).ask()

            if choice == "Week 1":
                type = "capitalAttacksWeek1"
            elif choice == "Week 2":
                type = "capitalAttacksWeek2"
            elif choice == "Week 3":
                type = "capitalAttacksWeek3"
            elif choice == "Week 4":
                type = "capitalAttacksWeek4"

            clan_data = update_datas(type, clan_data)

        elif user_choice == "Reset scores":
            clan_data = reset_score_menu(clan_data)

        elif user_choice == "Exit":
            break

    console.print("[bold yellow]Goodbye![/bold yellow]")