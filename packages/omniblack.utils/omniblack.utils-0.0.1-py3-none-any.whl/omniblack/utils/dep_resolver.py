from public import public

@public
def resolver(items, process, is_ready):
    items = list(items)

    while items:
        next_items = []

        for item in items:
            if is_ready(item):
                process(item)
            else:
                next_items.append(item)

        if len(items) == len(next_items):
            raise RuntimeError('No changes in resolver interation.')

        items = next_items


