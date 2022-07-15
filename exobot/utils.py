import json
from discord import Status
from dotenv import dotenv_values


def read_env_file(path):
    return dotenv_values(path)


def read_json_file(path):
    with open(path) as p:
        return json.load(p)


def format_date(date):
    return date.strftime("%A, %B %d %Y %H:%M")


def safe_list_get(lst, index, default):
    try:
        return lst[index]
    except IndexError:
        return default


def online_members(guild):
    return sum(member.status != Status.offline for member in guild.members)