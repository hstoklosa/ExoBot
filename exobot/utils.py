import json
from discord import Status


def read_json_file(path_to_file):
    with open(path_to_file) as p:
        return json.load(p)


def format_date(date):
    return date.strftime("%A, %B %d %Y %H:%M")


def online_members(guild):
    return sum(member.status != Status.offline for member in guild.members)