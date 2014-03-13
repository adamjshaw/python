import numpy as np
import sys
import math
u_data = open(sys.argv[3]+'-uvectors.txt','w')
v_data = open(sys.argv[3]+'-vvectors.txt','w')
out_vals = open(sys.argv[3]+'-values.txt','w')


def orthogonalize(r, vectors):
    if len(vectors) == 0:
        return r
    for vector in vectors:
        #tmp = #vector#.transpose()#
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
    in_m = np.matrix(np.loadtxt(open(sys.argv[3],'rb')))
    k = int(sys.argv[1])
    epsilon = float(sys.argv[2])
    vectors = []
    u_vectors = []
    values = []
    d = {}
    frequency = 1
    m = in_m.transpose()*in_m
    #print m.shape#np.linalg.eig(m)
    #for iterations in range(k)
    while len(vectors) < k:
        found = True
        r = np.random.random_sample(m.shape[0])*.25
        if len(vectors) > 0:
            m = m - values[len(vectors)-1]*(vectors[len(vectors)-1]*(vectors[len(vectors)-1].transpose()))
        for vector in vectors:
            tmp = np.array(vector).flatten()
            #print r.shape, vectors[i].shape, np.dot(vectors[i],r).shape
            r -= (np.dot(tmp,r))*tmp
        r = np.matrix(r).transpose()
        ortho = 1
        while(1):
            #print m.shape,r.shape
            new_r = m*r/np.linalg.norm(m*r)
            ep = np.linalg.norm(r - new_r)
            em = np.linalg.norm(r + new_r)
            r = new_r
            if ep < epsilon or em < epsilon:
                #if iterations == 0 or 
                break
            if similar(r,vectors):
                ortho += 1
                continue

            if ortho > 600:
                found = False
                break
            if ortho % frequency == 0:
                #r = np.array(r).flatten()
                r = orthogonalize(r,vectors)#for vector in vectors:
                    #tmp = vector.transpose()#np.array(vector).flatten()
                    #r -= (np.dot(tmp,r))*tmp
                #r = np.matrix(r).transpose()
            ortho += 1
        #if similar(r, vectors):
        #    frequency = int(frequency* 1.25)
        #    continue
        #print r
        if not found:
            print "not found"

            continue
        v = eigenvalue(m,r)
        if vsimilar(v, values) and similar(r, vectors):
            frequency = int(frequency * 1.1)
            #print frequency
            continue
        #print len(vectors)
        vectors.append(r)
        u_vectors.append(in_m*r/np.linalg.norm(in_m*r))
        values.append(v)
        d[v] = r
        #print v
        frequency = int(frequency*1.1)
    #values = sorted(values,reverse=True)
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
    print u_vectors.shape,v_vectors.shape
    u_vectors = [np.array(v).flatten() for v in u_vectors]
    v_vectors = v_vectors.transpose()
    v_vectors = [np.array(v).flatten() for v in v_vectors]
    print u_vectors[0].shape,v_vectors[0].shape
    print math.sqrt(frobenius)

    u_data.write('\n'.join(' '.join(repr(float(item))for item in row)for row in u_vectors)+'\n')
    v_data.write('\n'.join(' '.join(repr(float(item))for item in row)for row in v_vectors)+'\n')
    for v in values:
        out_vals.write(str(v))
        out_vals.write('\n')
    #print values

if __name__ == "__main__":
    main()

    
