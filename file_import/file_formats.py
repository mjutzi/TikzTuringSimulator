import re

DEFAULT_IGNORE_LINE = re.compile('(\s*)|(\s*#.*)')

# num_of_bands|num_of_states|chars_in|chars_out|empty_char|accepted_states(|initial_state)(;)
DEFAULT_HEADER_PATTERN = re.compile('(?P<num_of_bands>\d+)\s*[|]'
                                    '(?P<num_of_states>\d+)\s*[|]'
                                    '(?P<chars_in>[^|]+)\s*[|]'
                                    '(?P<chars_out>[^|]+)\s*[|]'
                                    '(?P<empty_char>[^|]+)\s*[|]'
                                    '(?P<accepted_states>[^|]+)\s*[|]'
                                    '((?P<initial_state>[^|]+)\s*[|])?'
                                    ';?')

# current_state,read_chars>new_state,new_chars,head_directions
DEFAULT_COMMAND_PATTERN = re.compile('\s*(?P<current_state>[^,\s]+)\s*,'
                                     '\s*(?P<read_chars>[^>]+)\s*>'
                                     '\s*(?P<new_state>[^,\s]+)\s*,'
                                     '\s*(?P<new_chars>[^LR]+)\s*,'
                                     '\s*(?P<head_directions>[LRN\s,]+)\s*')

CUSTOM_IGNORE_LINE = re.compile('(\s*)|(\s*#.*)')

# num_of_bands='12' chars_in={..} chars_out={..} empty_char='..' initial_state='..' accepted_states={..}
CUSTOM_HEADER_PATTERN = re.compile('\s*num_of_bands=\'(?P<num_of_bands>\d+)\'\s+'
                                   'chars_in={(?P<chars_in>[^}]+)}\s+'
                                   'chars_out={(?P<chars_out>[^}]+)}\s+'
                                   'empty_char=\'(?P<empty_char>[^\'])\'\s+'
                                   'initial_state=\'(?P<initial_state>[^\'])\'\s+'
                                   'accepted_states={(?P<accepted_states>[^}]+)}\s*')

# current_state: [read_chars] > new_state: [new_chars] [head_directions]
CUSTOM_COMMAND_PATTERN = re.compile('\s*(?P<current_state>[^:]+):'
                                    '\s\[(?P<read_chars>[^\]]+)\]\s*>'
                                    '\s*(?P<new_state>[^:]+):'
                                    '\s\[(?P<new_chars>[^\]]+)\]'
                                    '\s*\[(?P<head_directions>[^\]]+)\]')
