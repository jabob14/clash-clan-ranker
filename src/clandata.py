import coc
from filehandler import read_from_file, write_to_file
from scorelogic import sort_members_by_score, update_score, reset_scores

async def get_member_data(members):
    member_list = {}
    current_member_data = get_current_member_data()
    current_members = current_member_data.keys()
    for member in members:
        current_member = member.tag

        member_info = {
                        "name": member.name,
                        "townhall": member.town_hall,
                        "donations": member.donations,
                    }

        if current_member not in current_members:
            member_info["clanGamesScore"] = 0
            member_info["clanWarLeagueStars"] = 0
            member_info["capitalAttacks"] = 0
            member_info["totalScore"] = 0
        else:
            member_info["clanGamesScore"] = current_member_data[current_member]["clanGamesScore"]
            member_info["clanWarLeagueStars"] = current_member_data[current_member]["clanWarLeagueStars"]
            member_info["capitalAttacks"] = current_member_data[current_member]["capitalAttacks"]
            member_info["totalScore"] = current_member_data[current_member]["totalScore"]
            

        member_list[current_member] = member_info
    return member_list

async def get_clan_data(clan):
    clan_info = {
                "name": clan.name,
                "level": clan.level,
                "members": clan.member_count,
                "description" : clan.description,
                "badge" : clan.badge.url
            }
    return clan_info

async def update_data(COC_EMAIL, COC_PASSWORD, CLAN_TAG):
    async with coc.Client() as client:
        
        await client.login(COC_EMAIL, COC_PASSWORD)

        if not coc.utils.is_valid_tag(CLAN_TAG):
            print(f"Error: '{CLAN_TAG}' is not a valid clan tag.")
            return

        try:
            clan = await client.get_clan(CLAN_TAG)
            clan_info = await get_clan_data(clan)
            member_info =  await get_member_data(clan.members)

            member_info = update_score(member_info)
            member_info = sort_members_by_score(member_info)

            write_to_file(clan_info, member_info)
            

        except coc.NotFound:
            print(f"Clan with tag {CLAN_TAG} was not found.")
        except coc.Maintenance:
            print("The Clash of Clans API is currently in a maintenance break.")
        except Exception as e:
            print(f"An unexpected error occurred while fetching clan data: {e}")
        return []

def get_current_member_data():
    clan_data = read_from_file()
    member_data = clan_data["memberInfo"]
    return member_data

def reset_data():
    clan_data = read_from_file()
    clan_info = clan_data['clanInfo']
    member_list = reset_scores()
    member_list = sort_members_by_score(member_list)
    write_to_file(clan_info, member_list)
