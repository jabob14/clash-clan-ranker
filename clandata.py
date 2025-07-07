import coc

async def get_member_data(members):
    member_list = {}

    for member in members:
        current_member = member.tag
        member_info = {
                    "name": member.name,
                    "town_hall": member.town_hall,
                    "donations": member.donations,
                }
        member_list[current_member] = member_info
    return member_list

async def get_clan_data(clan):
    clan_info = {
                "name": clan.name,
                "level": clan.level,
                "members": clan.member_count,
                "description" : clan.description,
                "banner" : clan.badge.url
            }
    return clan_info

async def update_data(client, clan_tag):
    if not coc.utils.is_valid_tag(clan_tag):
        print(f"Error: '{clan_tag}' is not a valid clan tag.")
        return

    try:
        clan = await client.get_clan(clan_tag)
        print(f"Successfully fetched clan: '{clan.name}' ({clan.tag})")


        clan_info = await get_clan_data(clan)
        member_info =  await get_member_data(clan.members)

        clan_data = {
            "clanInfo" : clan_info,
            "memberInfo" : member_info
        }

    
        return clan_data

    except coc.NotFound:
        print(f"Clan with tag {clan_tag} was not found.")
    except coc.Maintenance:
        print("The Clash of Clans API is currently in a maintenance break.")
    except Exception as e:
        print(f"An unexpected error occurred while fetching clan data: {e}")
    
    return []
