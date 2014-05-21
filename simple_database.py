import sys

database = [{}]
fq = {}

def level():
    return len(database)-1

def incr_fq():
    pass

def decr_fq():
    pass

def end():
    sys.exit(0)

def set_name(name, val):
    for lvl in range(len(database)-1, -1, -1):
        if database[lvl]:
            if name in database[lvl]:
                prev_val = database[lvl][name]
                fq[prev_val] -= 1
                fq[val] = 1
            else:
                if val in fq:
                    fq[val] += 1
                else:
                    fq[val] = 1
        elif lvl == 0:
            fq[val] = 1

    database[level()][name] = val

def get(name):
    for lvl in range(len(database)-1, -1, -1):
        if name in database[lvl]:
            return database[lvl][name]
            
    return 'NULL'

def begin():
    database.append({})

def rb_val(i, lvl):
    return database[level()-lvl].get(i[0])

def rollback():
    if level() == 0:
        return 'NO TRANSACTION'

    items = database[level()].items()
    for i in items:
        if i[1] != 'NULL':
            fq[i[1]] -= 1    
        if database[level()-1]:
            fq[rb_val(i, 1)] += 1
        elif database[level()-2] and level()-2 >= 0:
            fq[rb_val(i, 2)] += 1

    database.remove(database[level()])

def commit():
    if level() == 0:
        return 'NO TRANSACTION'
    else:
        for lvl in (range(len(database)-1, 0, -1)):
            database[lvl-1].update(database[lvl])
            database.remove(database[lvl])

def unset(name):
    prev_val = get(name)
    fq[prev_val] -= 1
    database[level()][name] = "NULL"

def numequalto(val):
    if fq.get(val):
        return fq.get(val)
    return str(0)

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