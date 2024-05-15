from __future__ import annotations

import requests

from sopel import plugin
from sopel.config import types


class TraktSection(types.StaticSection):
    client_id = types.SecretAttribute('client_id', default=types.NO_DEFAULT)


def setup(bot):
    bot.config.define_section('trakt', TraktSection)


def configure(config):
    config.define_section('trakt', TraktSection, validate=False)
    config.trakt.configure_setting('client_id', 'Enter Trakt client ID: ')


class TraktException(Exception):
    pass


class NoUserSetException(TraktException):
    pass


class NoUserException(TraktException):
    pass


class NoHistoryException(TraktException):
    pass


class NoPublicHistoryException(NoHistoryException):
    pass


def format_episode_output(user, show, season, episode, title):
    pad_episode = str(episode).zfill(2)
    return f'{user} last watched: {show} {season}x{pad_episode} - {title}'


def format_movie_output(user, film, year):
    return f'{user} last watched: {film} ({year})'


def format_output(user, json):
    if json['type'] == 'episode':
        return format_episode_output(user,
                                     json['show']['title'],
                                     json['episode']['season'],
                                     json['episode']['number'],
                                     json['episode']['title'])
    if json['type'] == 'movie':
        return format_movie_output(user,
                                   json['movie']['title'],
                                   json['movie']['year'])


def get_trakt_user(arg, nick, db):
    if arg:
        return arg

    trakt_user = db.get_nick_value(nick, 'trakt_user')
    if trakt_user:
        return trakt_user

    raise NoUserSetException


def get_api_url(user):
    return f'https://api.trakt.tv/users/{user}/history'


def get_headers(client_id):
    return {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': client_id
    }


def get_last_play(response):
    if response.status_code == 404:
        raise NoUserException('User does not exist')

    if response.status_code == 401:
        raise NoPublicHistoryException("User's profile is private")

    if len(response.json()) == 0:
        raise NoHistoryException('User has no history')

    return response.json()[0]


@plugin.commands('trakt')
def trakt_command(bot, trigger):
    client_id = bot.config.trakt.client_id

    try:
        user = get_trakt_user(trigger.group(3), trigger.nick, bot.db)
    except NoUserSetException:
        bot.reply(
            "User not set; use {}traktset or pass user as argument"
            .format(bot.config.core.help_prefix)
        )
        return

    api_url = get_api_url(user)
    headers = get_headers(client_id)
    r = requests.get(api_url, headers=headers)

    try:
        last_play = get_last_play(r)
    except (NoUserException, NoHistoryException) as e:
        bot.say(str(e))
        return

    out = format_output(user, last_play)
    bot.say(out)


@plugin.commands('traktset')
def traktset(bot, trigger):
    user = trigger.group(2)

    if not user:
        bot.say('no user given')
        return

    bot.db.set_nick_value(trigger.nick, 'trakt_user', user)

    bot.say(f'{trigger.nick}\'s trakt user is now set as {user}')
