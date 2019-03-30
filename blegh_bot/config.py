from blegh_bot.constants import CONFIG_FILE

import yaml

_MINIMUM_SECTIONS = ['reddit']


class ConfigError(Exception):
    pass


def parse_config_file(fp):
    with open(fp) as infile:
        return yaml.safe_load(infile)


def verify_config(parsed):
    try:
        assert all((
            k in parsed.keys() for k in _MINIMUM_SECTIONS
        ))
        return parsed
    except AssertionError:
        ConfigError('ensure all values in {} present in config file'.format(_MINIMUM_SECTIONS))


_parsed = verify_config(parse_config_file(CONFIG_FILE))

file_config = _parsed
