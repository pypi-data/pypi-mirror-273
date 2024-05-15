# sopel-trakt

A Sopel plugin to fetch users' recent Trakt plays

## Installation

Can be installed from PyPI using:

    pip install sopel-trakt

## Configuration

`sopel-trakt` has one required configuration value: your API app's client ID.
You can run `sopel-plugins configure trakt` to set it interactively, or add a
section for this plugin to your bot's `.cfg` file directly:

```ini
[trakt]
client_id = LongRandomStringProvidedByTrakt
```

Create or retrieve your Trakt API app's client ID at https://trakt.tv/oauth/applications

## Testing

If you would like to make a contribution, be sure to run the included tests. Test requirements can be installed using:

    pip install -r dev-requirements.txt

run tests using:

    make test

## Credits

Adopted from a Sopel 6 plugin, `sopel_modules.trakt`: https://github.com/surskitt/sopel-trakt
