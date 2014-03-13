import numpy as np
import sys
import math
out_data = open(sys.argv[3]+'-vectors.txt','w')
out_vals = open(sys.argv[3]+'-values.txt','w')


def orthogonalize(r, vectors):
    if len(vectors) == 0:
        return r
    for vector in vectors:
        tmp = np.array(vector).flatten()
        arr = np.array(r).flatten()
        r -= (np.dot(tmp,arr))*vector
    return r
def vsimilar(v, values):
    if len(values) > 0:
        for prev in values:
            if math.fabs((math.fabs(v) - math.fabs(prev)) / v) < 0.01:
                return True
    return False
def similar(r, vectors):
    if len(vectors) > 0:
        for v in vectors:
            if math.fabs((math.fabs(r[0]) - math.fabs(v[0])) / r[0]) < 0.02:
                return True
    return False

def eigenvalue(m,r):
    t = m*r
    for i in range(r.shape[0]):
        if r[i] != 0:
            return float(t[i]/r[i])
    return 0

def main():
    m = np.matrix(np.loadtxt(open(sys.argv[3],'rb')))
    print np.linalg.eig(m)
    k = int(sys.argv[1])
    epsilon = float(sys.argv[2])
    vectors = []
    values = []
    d = {}
    frequency = 1
    orthos = []
    while len(vectors) < k:
        found = True
        r = np.random.random_sample(m.shape[0])*.25
        if len(vectors) > 0:
            m = m - values[len(vectors)-1]*(vectors[len(vectors)-1]*(vectors[len(vectors)-1].transpose()))
        for vector in vectors:
            tmp = np.array(vector).flatten()
            r -= (np.dot(tmp,r))*tmp
        r = np.matrix(r).transpose()
        ortho = 1
        while(1):
            new_r = m*r/np.linalg.norm(m*r)
            ep = np.linalg.norm(r - new_r)
            em = np.linalg.norm(r + new_r)
            r = new_r
            if ep < epsilon or em < epsilon:
                break
            if similar(r,vectors):
                ortho += 1
                continue

            if ortho > 600:
                found = False
                break
            if ortho % frequency == 0:
                r = orthogonalize(r,vectors)
            ortho += 1
        if not found:
            print "not found"

            continue
        v = eigenvalue(m,r)
        if vsimilar(v, values) and similar(r, vectors):
            frequency = int(frequency * 1.25)
            continue
        print len(vectors)
        vectors.append(r)
        orthos.append(ortho)
        values.append(v)
        d[v] = r
        frequency = int(frequency*1.25)
    vectors = [np.array(v) for v in vectors]
    out_data.write('\n'.join(' '.join(repr(float(item))for item in row)for row in vectors)+'\n')
    for v in values:
        out_vals.write(str(v))
        out_vals.write('\n')
    print sum(orthos)/float(len(orthos))

if __name__ == "__main__":
    main()

    
