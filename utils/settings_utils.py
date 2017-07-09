import os
import re


def _load_dict(path):
    if not os.path.isfile(path):
        return {}

    item_pattern = re.compile('(?P<key>[^\s:]+):\s*(?P<value>.+)\s*')

    def key(match):
        return match.group('key')

    def value(match):
        return match.group('value')

    with open(path, 'r') as file:
        matches = [item_pattern.match(line) for line in file.readlines()]
        return {key(m): value(m) for m in matches if m}


def _copy_or_empty(dict):
    return dict.copy() if dict else {}


def load_settings(settings_file, default_settings=None):
    def_settings = _load_dict(settings_file)
    all_settings = _copy_or_empty(default_settings)
    all_settings.update(def_settings)

    return all_settings
