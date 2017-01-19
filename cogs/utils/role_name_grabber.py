import discord

async def role_name_grabber(member):
    role_list = []
    for role in member.roles:
        role_list.append(role.name)
    return role_list