def schedule_day_offs(df):
    master_dict = {}
    specialists = set()
    juniors = set()
    name_to_bunk = {}

    for _, row in df.iterrows():
        name = row['Name'].strip()
        role = row['Role'].strip().lower()
        prefs = [row['Pref1'].strip(), row['Pref2'].strip(), row['Pref3'].strip()]
        master_dict[(name, role)] = prefs

        if role == 'specialist':
            specialists.add(name)
        elif role == 'junior':
            juniors.add(name)
        else:
            name_to_bunk[name] = role

    assignments = {
        'Specialist': set(),
        'GC1': set(),
        'GC2': set(),
        'JC': set()
    }

    for name in specialists:
        assignments['Specialist'].add(name)
    for name in juniors:
        assignments['JC'].add(name)

    for (name, role), prefs in master_dict.items():
        if name in specialists or name in juniors:
            continue

        assigned = False
        for pref in prefs:
            for group in ['GC1', 'GC2']:
                if pref in assignments[group] and not is_bunk_conflict(name, assignments[group], name_to_bunk):
                    assignments[group].add(name)
                    assigned = True
                    break
            if assigned:
                break

        if not assigned:
            gc1_conflict = is_bunk_conflict(name, assignments['GC1'], name_to_bunk)
            gc2_conflict = is_bunk_conflict(name, assignments['GC2'], name_to_bunk)
            if not gc1_conflict and len(assignments['GC1']) <= len(assignments['GC2']):
                assignments['GC1'].add(name)
            elif not gc2_conflict:
                assignments['GC2'].add(name)
            else:
                (assignments['GC1'] if len(assignments['GC1']) <= len(assignments['GC2']) else assignments['GC2']).add(name)

    return {group: sorted(names) for group, names in assignments.items()}

def is_bunk_conflict(name, group, name_to_bunk):
    my_bunk = name_to_bunk.get(name)
    return any(name_to_bunk.get(other) == my_bunk for other in group)
