import sys

database = [{}]

def level():
    return len(database)-1

def end():
    sys.exit(0)

def set_name(name, val):
    database[level()][name] = val

def get(name):
    for lvl in range(len(database)-1, -1, -1):
        if name in database[lvl]:
            return database[lvl][name]
            
    return 'NULL'

def begin():
    database.append({})

def rollback():
    if level() == 0:
        return 'NO TRANSACTION'
    else:
        database.remove(database[level()])

def commit():
    if level() == 0:
        return 'NO TRANSACTION'
    else:
        for lvl in (range(len(database)-1, 0, -1)):
            database[lvl-1].update(database[lvl])
            database.remove(database[lvl])

def unset(name):
    database[level()][name] = "NULL"

def numequalto(val):
    count = 0
    i = 0

    for name, value in database[i].iteritems():
        if value == val:
            if database[level()].get(name) == 'NULL':
                count = 0
            else:
                count += 1
                i += 1

    return str(count)

if __name__ == "__main__":
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
                data = switch[cmd[0]]()
            elif len(cmd) == 2:
                data = switch[cmd[0]](cmd[1])
            elif len(cmd) == 3:
                data = switch[cmd[0]](cmd[1], cmd[2])
        if data:
            sys.stdout.write(str(data) + '\n')
        else:
            pass


    print database
