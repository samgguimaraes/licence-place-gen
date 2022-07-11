import logging
import random
import rstr

def random_pick(rtype: str,
                options: dict):
    '''Pick a random element from the list following the given method
    '''
    if rtype == 'random.params':
        return None
    options = options.copy()
    params = options.pop('params')
    if rtype == 'random.linear':
        delta = params[1] - params[0]
        pick = random.random() * delta + params[0]
        for _, option in options.items():
            option = option.copy()
            val = option.pop('random.params', params[1])
            if val > pick:
                return get_values(option)
    
    logging.warning(f'No value picked for {rtype}')
    return (None, None)


def replace_value(value,
                  value_keys: dict):
    '''Replace all ocurences of $ taged strings with the equivalend in the value_keys dictionary
            If the value is a regular expression (prefix 'reg:') a string is generated from it
    '''
    if type(value) is dict:
        return get_values(value, value_keys)[0]
    elif type(value) is list:
        return [replace_value(v, value_keys) for v in value]
    elif type(value) is not str:
        return value
    if value.startswith('reg:'):
        return rstr.xeger(value[len('reg:'):])
    elif value.startswith('$'):
        target = value[1:]
        return value_keys.get(target, value)
    else:
        return value


def get_values(val_dict: dict,
               value_keys:dict = {}):
    '''Recursively resolve all value replacements and random pick from a dictionary
        Returns the resolved dictonary and the dictionary containing the keys gathered
    '''
    result = {}
    value_keys = value_keys.copy()
    for key, value in val_dict.items():
        if key == 'vars':
            for v in value:
                new_keys, old_keys = get_values(v, value_keys)
                if new_keys:
                    value_keys.update(new_keys)
                if old_keys:
                    value_keys.update(old_keys)
        elif str(key).startswith('random.'):
            value, vk = random_pick(key, value)
            if value:
                result.update(value)
            if vk:
                value_keys.update(vk)
        elif type(value) is str:
            result[key] = replace_value(value, value_keys)
        elif type(value) is list:
            result[key] = [replace_value(v, value_keys) for v in value]
        elif type(value) is dict:
            values, vks = get_values(value, value_keys)
            result[key] = values
            if vks:
                value_keys.update(vks)
        else:
            result[key] = value
                    
    return result, value_keys