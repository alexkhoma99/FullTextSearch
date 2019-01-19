import app.globals
import sys

def invertedIndex(sfname):
    client = app.globals.client
    db = app.globals.db
    iidx = app.globals.iidx
    with open('uploads/' + sfname, 'r', errors='ignore') as f:
        line = f.readline()
        c = 0
        while line:
            temp = line.strip()
            if c == 0:
                j = {
                    'filename':sfname,
                    'Line0':temp
                }
                db.docs.insert_one(j)
            else:
                j = {
                    'Line{}'.format(c): temp
                }
                db.docs.update_one({'filename':sfname}, {"$set": j})

            for word in temp.strip(' .').split():
                word = word.lower()
                if word in iidx:
                    iidx[word].append((sfname, c))
                else:
                    iidx[word] = [(sfname, c)]
            line = f.readline()
            c += 1
    for k,v in iidx.items():
        continue
        #print(str(k) + " : " + str(v), file=sys.stderr)

def search(term):
    client = app.globals.client
    db = app.globals.db
    iidx = app.globals.iidx
    res = app.globals.res
    res = []
    if term not in iidx:
        return []
    else:
        print("OCCURRENCES: " + str(iidx[term]))
        for occ in iidx[term]:
            for d in db.docs.find({'filename':occ[0]}):
                #print(d, file=sys.stderr)
                res.append( ( occ[0], str(occ[1]), d['Line'+str(occ[1])]) )
    print("res: " + str(res), file=sys.stderr)
    return res
