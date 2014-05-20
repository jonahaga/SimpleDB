import sys

database = [{}]
current_level = 0

def end():
    sys.exit(0)

def set_name(name, val):
    database[current_level][name] = val

def get(name, *args):
    for lvl in range(len(database)-1, -1, -1):
        if args:
            if name in database[lvl]:
                return database[lvl][name]
            else:
                pass
        else:
            if name in database[lvl]:
                sys.stdout.write(database[lvl][name] + '\n')
                return
            
    if not args:
        sys.stdout.write("NULL\n")                

def begin():
    database.append({})
    global current_level
    current_level += 1

def rollback():
    global current_level
    if current_level == 0:
        sys.stdout.write("NO TRANSACTION\n")
    else:
        database.remove(database[current_level])
        current_level -= 1

def commit():
    global current_level 
    if current_level == 0:
        sys.stdout.write("NO TRANSACTION\n")
    else:
        for lvl in (range(len(database)-1, 0, -1)):
            database[lvl-1].update(database[lvl])
            database.remove(database[lvl])

    current_level = 0

def unset(name):
    database[current_level][name] = "NULL"

def numequalto(val):
    count = 0
    i = 0

    for name, value in database[i].iteritems():
        if value == val:
            if get(name, val) == val:
                count += 1
            elif get(name, val) == 'NULL':
                count = 0
        i += 1

    sys.stdout.write(str(count) + '\n')

for line in sys.stdin:
    cmd = line.split()
    switch = {'BEGIN': begin,
              'ROLLBACK': rollback,
              'COMMIT': commit,
              'SET': set_name,
              'GET': get,
              'UNSET': unset,
              'NUMEQUALTO': numequalto,
              'END': end }
    
    if cmd[0] in switch:
        if len(cmd) == 1:
            switch[cmd[0]]()
        elif len(cmd) == 2:
            switch[cmd[0]](cmd[1])
        elif len(cmd) == 3:
            switch[cmd[0]](cmd[1], cmd[2])
    else:
        pass