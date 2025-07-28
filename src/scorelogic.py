from config import *
from clandata import read_from_file

def update_score(member_list):
    top_donator = find_top_donator(member_list)
    for member in member_list:
        clan_game_score = calculate_clan_game_score(member_list[member]['clanGamesScore'])
        member_list[member]['capitalAttacks'] = calculate_capital_attack_total(member_list, member)
        raid_score = member_list[member]['capitalAttacks'] * CAPITAL_RAID_REWARD
        cwl_score = member_list[member]['clanWarLeagueStars'] * CWL_STAR_REWARD
        total_score = clan_game_score + raid_score + cwl_score
        if top_donator == member:
            total_score += TOP_DONATOR_BONUS
        member_list[member]['totalScore'] = total_score
    return member_list


def find_top_donator(member_list):
    top_donator = None
    for member in member_list:
        if top_donator == None:
            top_donator = member
        else:
            if member_list[member]['donations'] > member_list[top_donator]['donations']:
                top_donator = member
    return top_donator


def calculate_capital_attack_total(member_list, member):
    total_attacks = 0
    total_attacks += member_list[member]['capitalAttacksWeek1']
    total_attacks += member_list[member]['capitalAttacksWeek2']
    total_attacks += member_list[member]['capitalAttacksWeek3']
    total_attacks += member_list[member]['capitalAttacksWeek4']
    return total_attacks


def calculate_clan_game_score(clan_game_points):
    if clan_game_points >= 4000:
        clan_game_score = CLAN_GAMES_REWARD * clan_game_points
        clan_game_score += MAXED_CLAN_GAMES_BONUS
    else:
        clan_game_score = CLAN_GAMES_REWARD * clan_game_points
    return clan_game_score


def sort_members_by_score(member_list):
    member_items = member_list.items()
    sorted_members = sorted(member_items, key=lambda item: (item[1]['totalScore'], item[1]['donations']), reverse=True)
    sorted_member_info_dict = dict(sorted_members)
    return sorted_member_info_dict


def reset_scores(member_list):
    for member in member_list:
        member_list[member]['clanGamesScore']       = 0
        member_list[member]['clanWarLeagueStars']   = 0
        member_list[member]['capitalAttacksWeek1']  = 0
        member_list[member]['capitalAttacksWeek2']  = 0
        member_list[member]['capitalAttacksWeek3']  = 0
        member_list[member]['capitalAttacksWeek4']  = 0
    return update_score(member_list)
