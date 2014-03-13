import numpy as np
import sys
import math
a_data = open('matrix-rank'+sys.argv[1]+'.txt','w')
missing_data = open('matrix-rank'+sys.argv[1]+'-missing.txt','w')

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
    k = int(sys.argv[1])
    epsilon = 0.01
    p = float(sys.argv[2])
    in_m = []
    ls = []
    rs = []
    for i in range(k):
        l_vec = np.random.random_sample((30,))
        r_vec = np.random.random_sample((30,))
        ls.append(l_vec)
        rs.append(r_vec)
    s_vals = np.random.random_sample((k,))
    l_vectors = np.matrix(np.array(ls)).transpose()
    r_vectors = np.matrix(np.array(rs))
    s_matrix = np.matrix(np.zeros((k,k)))
    for i in range(len(s_vals)):
        s_matrix[i,i] = float(s_vals[i])
    in_m = l_vectors*s_matrix*r_vectors
    write_m = np.array(in_m)
    a_data.write('\n'.join(' '.join(repr(float(item))for item in row)for row in write_m)+'\n')
    m = np.matrix(np.zeros((30,30)))
    mu = np.matrix.mean(in_m)
    m += mu
    for i in range(30):
        for j in range(30):
            if np.random.random() < p:
                m[i,j] = in_m[i,j]
    write_missing = np.array(m)
    missing_data.write('\n'.join(' '.join(repr(float(item))for item in row)for row in write_missing)+'\n')
    vectors = []
    u_vectors = []
    values = []
    d = {}
    frequency = 1
    m = in_m.transpose()*in_m
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
            frequency = int(frequency * 1.1)
            continue
        vectors.append(r)
        u_vectors.append(in_m*r/np.linalg.norm(in_m*r))
        values.append(v)
        d[v] = r
        frequency = int(frequency*1.1)
    u_vectors = np.matrix(np.array(u_vectors)).transpose()
    v_vectors = np.matrix(np.array(vectors))
    s_values = np.matrix(np.array(values))
    s = np.matrix(np.zeros((k,k)))
    for i in range(len(values)):
        s[i,i] = values[i]
    decomp = u_vectors*s*v_vectors
    frobenius = 0
    for i in range(in_m.shape[0]):
        for j in range(in_m.shape[1]):
            frobenius += (in_m[i,j] - decomp[i,j])**2
    u_vectors = [np.array(v).flatten() for v in u_vectors]
    v_vectors = v_vectors.transpose()
    v_vectors = [np.array(v).flatten() for v in v_vectors]
    print math.sqrt(frobenius)


if __name__ == "__main__":
    main()

    
