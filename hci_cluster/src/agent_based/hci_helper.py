

def parse_multi_list(string_table):
    """
    Parse list with repeating objects
    """

    entries = []
    start = False
    entry = {}


    for line in string_table:
        if len(line) == 1:
            #Skip invalid lines
            continue

        key, value = line[0].strip(), line[1].strip()
        if not start:
            start = key
            entry[key] = value
        elif start:
            if key == start:
                entries.append(entry)
                entry = {}
                start = key
            entry[key] = value
    # Add last key also
    entries.append(entry)
    return entries

def parse_list(string_table, field):
    """
    Parse Powershell lists
    """
    seperator = False
    entries = {}
    content = {}

    for line in string_table:
        if len(line) == 1:
            # Skip Invalid lines
            continue
        key, value = line[0].strip(), line[1].strip()
        if not seperator:
            # First line we hit, is gone be the seperator
            # between the blocks of information
            seperator = key
        if key == seperator:
            # Current List Key is the Seperator,
            # we start a new dict for the folowing content
            # When we had content already for the round before,
            # we save it to our entires dict. Item is gone be the
            # content of the seperator field
            if content:
                item = content[field]
                del content[field]
                if item:
                    entries[item] = content
            content = {}
        content[key] = value

    # In ordner to not miss the last entry, we
    # check the same stuff again and update the entries dict
    # if needed
    if content:
        item = content[field]
        del content[field]
        if item:
            entries[item] = content
    return entries
