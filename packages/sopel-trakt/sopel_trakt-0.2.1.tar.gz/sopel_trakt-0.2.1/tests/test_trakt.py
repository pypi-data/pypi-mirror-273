from __future__ import annotations

import pytest
import unittest
import unittest.mock

import sopel_trakt as trakt


def test_format_episode_output():
    expected = 'testuser last watched: show 1x01 - title'

    out = trakt.format_episode_output('testuser', 'show', '1', '1', 'title')

    assert expected == out


def test_format_movie_output():
    expected = 'testuser last watched: film (year)'

    out = trakt.format_movie_output('testuser', 'film', 'year')

    assert expected == out


@unittest.mock.patch('sopel_trakt.format_episode_output')
@unittest.mock.patch('sopel_trakt.format_movie_output')
def test_format_output_episode(mock_movie_format, mock_ep_format):
    json = {
        'type': 'episode',
        'show': {'title': 'title'},
        'episode': {
            'season': 'season',
            'number': 'episode',
            'title': 'title'
        }
    }

    trakt.format_output('testuser', json)

    mock_ep_format.assert_called_once()
    assert not mock_movie_format.called


@unittest.mock.patch('sopel_trakt.format_episode_output')
@unittest.mock.patch('sopel_trakt.format_movie_output')
def test_format_output_movie(mock_movie_format, mock_ep_format):
    json = {
        'type': 'movie',
        'movie': {
            'title': 'title',
            'year': 'year'
        }
    }

    trakt.format_output('testuser', json)

    mock_movie_format.assert_called_once()
    assert not mock_ep_format.called


def test_get_trakt_user_with_arg():
    expected = 'arg_user'
    out = trakt.get_trakt_user('arg_user', 'nick', 'mock_db')

    assert expected == out


def test_get_api_url():
    expected = 'https://api.trakt.tv/users/testuser/history'

    out = trakt.get_api_url('testuser')

    assert expected == out


def test_get_headers():
    expected = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': 'api_key'
    }

    out = trakt.get_headers('api_key')

    assert expected == out


def test_get_last_play():
    expected = 'lastplay'

    response = unittest.mock.MagicMock()
    response.json.return_value = ['lastplay']

    out = trakt.get_last_play(response)

    assert expected == out


def test_get_last_play_no_user():
    response = unittest.mock.MagicMock()
    response.status_code = 404

    with pytest.raises(trakt.NoUserException) as e:
        trakt.get_last_play(response)

    assert str(e.value) == 'User does not exist'


def test_get_last_play_no_history():
    response = unittest.mock.MagicMock()
    response.json.return_value = []

    with pytest.raises(trakt.NoHistoryException) as e:
        trakt.get_last_play(response)

    assert str(e.value) == 'User has no history'
