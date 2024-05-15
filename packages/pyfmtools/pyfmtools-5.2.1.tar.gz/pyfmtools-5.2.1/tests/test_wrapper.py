import numpy as np
import pyfmtools as pyfm
import random
import sys


r=3
n=3
env = pyfm.fm_init( n)
pyfm.isTest = True


A = pyfm.ShowCoalitions( env)
print( "Fuzzy measure wrt n=3 criteria has ",env.m," parameters ordered like this (binary order)")
print( A)
pyfm.fm_free( env);

ti=1
n=4
env = pyfm.fm_init( n)
size, v = pyfm.generate_fm_2additive_concave( ti,n, env)
print( "2-additive concave FM in Mobius and its length (n=4)")
print( v)
print("has ", size, " nonzero parameters ")

print("A convex FM in cardinality ordering ")
A = pyfm.ShowCoalitionsCard( env)
print( A)

size, v = pyfm.generate_fmconvex_tsort( ti, n, n-1 , 1000, 8, 1, env)
print( v)
print("has ", size, " nonzero parameters ")

vb = pyfm.ConvertCard2Bit( v, env)

print("a convex FM in binary ordering ")
A = pyfm.ShowCoalitions( env)
print( A)
print( vb)

r = pyfm.IsMeasureSupermodular( vb, env)
print( "Is it convex (test)?", r)
r = pyfm.IsMeasureAdditive( vb, env)
print("Is it additive (test)?", r)

mc = pyfm.export_maximal_chains( n, vb, env)
print( "Export maximal chains ")
print( mc)

x = [0.2,0.1,0.6,0.2]
z = pyfm.Choquet( x, vb, env)
print( "Choquet integral of ",x, " is ",z)

z = pyfm.Sugeno( x, vb, env)
print("Sugeno integral of ",x,  " is ",z)


###
# Test generated wrapper
###

# Test wrapper for:
#    double py_ChoquetKinter(double* x, double* v, int kint, struct fm_env* env)
x = [0.2,0.5,0.4]
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
kint = 2
r = pyfm.ChoquetKinter( x, v, kint, env)
print( "Choquet integral of: ", kint, x, v)
print( "equals: ", r)

# Test wrapper for:
#    double py_Orness(double* Mob, struct fm_env* env)
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
r = pyfm.Orness(v, env)
print( "orness value of the Choquet integral wrt fuzzy measure v: ", v)
print( "equals: ", r)

# Test wrapper for:
#    void py_NonmodularityIndexKinteractive(double* v, double* out_w, int kint,  struct fm_env* env)
kint = 2
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
pnm = pyfm.NonmodularityIndexKinteractive( v, kint, env)
print( "nonmodularity indices of k-interactive fuzzy measure v: ", kint, v)
print( "equals: ", pnm)


# Test wrapper for:
#    double py_min_subset(double* x, int n, int_64 S)
x = [0,0.3,0.5,0.6,0.7,0.8,0.85,0.9]
n = len( x)
S = 6
min = pyfm.min_subset( x, n, S)
print( "x: ", x)
print( "n: ", n)
print( "S: ", S)
print( "min: ", min)


# Test wrapper for:
#    double py_max_subset(double* x, int n, int_64 S)
# pyfm.max_subset(x, n, S)
x = [0,0.3,0.5,0.6,0.7,0.8,0.85,0.9]
n = len( x)
S = 5
max = pyfm.max_subset( x, n, S)
print( "x: ", x)
print( "n: ", n)
print( "S: ", S)
print( "max: ", max)

# Test wrapper for:
#    double py_min_subsetC(double* x, int n, int_64 S, struct fm_env* env)
x = [0,0.3,0.5]
n = len( x)
S = 3
min = pyfm.min_subsetC( x, n, S, env)
print( "x: ", x)
print( "n: ", n)
print( "S: ", S)
print( "min: ", min)

# Test wrapper for:
#    double py_max_subsetNegC(double* x, int n, int_64 S, struct fm_env* env)
x = [0,0.3,0.5]
n = len( x)
S = 3
max = pyfm.max_subsetNegC( x, n, S, env)
print( "x: ", x)
print( "n: ", n)
print( "S: ", S)
print( "max: ", max)

# Test wrapper for:
#    int py_SizeArraykinteractive(int n, int k, struct fm_env* env)
n = 3
k = 1
s = pyfm.SizeArraykinteractive(n, k, env)
print( "n: ", n)
print( "k: ", k)
print( "size: ", s)

# Test wrapper for:
#    int py_IsSubsetC(int i, int j, struct fm_env* env)
i = 2
j = 1
s = pyfm.IsSubsetC(n, k, env)
print( "i: ", i)
print( "j: ", j)
print( "size: ", s)

# Test wrapper for:
#    int py_IsElementC(int i, int j, struct fm_env* env)
i = 2
j = 1
s = pyfm.IsElementC(n, k, env)
print( "i: ", i)
print( "j: ", j)
print( "size: ", s)

# Test wrapper for:
#    void py_ExpandKinteractive2Bit(double* out_dest, double* src, struct fm_env* env, int kint, int arraysize)
src = [0.0340916, 0.01109779, 0.07918582,0.7,1]
kint = 1
dest = pyfm.ExpandKinteractive2Bit(src, env, kint)
print( "src: ", src)
print( "kint: ", kint)
print( "dest: ", dest)

# Test wrapper for:
#    void py_Shapley(double* v, double* out_x, struct fm_env* env)
# pyfm.Shapley(v, env)
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
x = pyfm.Shapley( v, env)
print( "v: ", v)
print( "x: ", x)

# Test wrapper for:
#    void py_Banzhaf(double* v, double* out_B, struct fm_env* env)
v =[0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
x = pyfm.Banzhaf(v, env)
print( "v: ", v)
print( "x: ", x)


# Test wrapper for:
#    void py_ShapleyMob(double* Mob, double* out_x, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
x = pyfm.ShapleyMob( Mob, env)
print( "Mob: ", Mob)
print( "x: ", x)


# Test wrapper for:
#    void py_BanzhafMob(double* Mob, double* out_B, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
x = pyfm.BanzhafMob(Mob, env)
print( "Mob: ", Mob)
print( "x: ", x)

# Test wrapper for:
#    double py_ChoquetMob(double* x, double* Mob, struct fm_env* env)
x =[0.6,0.3,0.8]
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
c = pyfm.ChoquetMob(x, Mob, env)
print( "Mob: ", Mob)
print( "x: ", x)
print( "Choquet integral: ", c )

# Test wrapper for:
#    void py_ConstructLambdaMeasure(double* singletons, double* out_lambdax, double* out_v, struct fm_env* env)
singletons = [0, 0.3, 0.5]
lambdax, v = pyfm.ConstructLambdaMeasure(singletons, env)
print( "singletons: ", singletons)
print( "lambdax, v: ", lambdax, v)

# Test wrapper for:
#    void py_ConstructLambdaMeasureMob(double* singletons, double* out_lambdax, double* out_Mob, struct fm_env* env)
singletons = [0, 0.3, 0.5]
lambdax, Mob = pyfm.ConstructLambdaMeasureMob(singletons, env)
print( "singletons: ", singletons)
print( "lambdax, Mob: ", lambdax, Mob)

# Test wrapper for:
#    void py_dualm(double* v, double* out_w, struct fm_env* env)
v =[0,0.3,0.5,0.6,0.4,0.8,0.7,1]
w = pyfm.dualm(v, env)
print( "v: ", v)
print( "w: ", w)

# Test wrapper for:
#    void py_dualmMob(double* v, double* out_w, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
w = pyfm.dualmMob(Mob, env)
print( "Mob: ", Mob)
print( "w: ", w)

# Test wrapper for:
#    double py_Entropy(double* v, struct fm_env* env)
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
r = pyfm.Entropy(v, env)
print( "v: ", v)
print( "r: ", r)

# Test wrapper for:
#    void py_FuzzyMeasureFit(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)
datanum = 10
additive = 2
dataset = np.random.uniform(low=0.0, high=1.0, size=(datanum * ( env.n + 1),))
res = pyfm.FuzzyMeasureFit(datanum, additive, env, dataset)
print( "datanum: ", datanum)
print( "additive: ", additive)
print( "dataset: ", dataset)
print( "res: ", res)

# Test wrapper for:
#    void py_FuzzyMeasureFitMob(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)
datanum = 10
additive = 3
dataset = np.random.uniform(low=0.0, high=1.0, size=(datanum * ( env.n + 1),))
res = pyfm.FuzzyMeasureFitMob(datanum, additive, env, dataset)
print( "datanum: ", datanum)
print( "additive: ", additive)
print( "dataset: ", dataset)
print( "res: ", res)

# Test wrapper for:
#    void py_FuzzyMeasureFitKtolerant(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)
datanum = 10
additive = 2
dataset = np.random.uniform(low=0.0, high=1.0, size=(datanum * ( env.n + 1),))
res = pyfm.FuzzyMeasureFitKtolerant(datanum, additive, env, dataset)
print( "datanum: ", datanum)
print( "additive: ", additive)
print( "dataset: ", dataset)
print( "res: ", res)

# Test wrapper for:
#    void py_FuzzyMeasureFitLPKmaxitive(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)
datanum = 10
additive = 2
dataset = np.random.uniform(low=0.0, high=1.0, size=(datanum * ( env.n + 1),))
res = pyfm.FuzzyMeasureFitLPKmaxitive(datanum, additive, env, dataset)
print( "datanum: ", datanum)
print( "additive: ", additive)
print( "dataset: ", dataset)
print( "res: ", res)

# Test wrapper for:
#    void py_FuzzyMeasureFitLPKinteractive(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K)
datanum = 10
additive = 2
K = 0.5
dataset = np.random.uniform(low=0.0, high=1.0, size=(datanum * ( env.n + 1),))
v = pyfm.FuzzyMeasureFitLPKinteractive(datanum, additive, env, K, dataset)
print( "datanum: ", datanum)
print( "additive: ", additive)
print( "K: ", K)
print( "dataset: ", dataset)
print( "v: ", v)


# Test wrapper for:
#    void py_FuzzyMeasureFitLPKinteractiveMaxChains(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K)
datanum = 10
additive = 2
K = 0.5
dataset = np.random.uniform(low=0.0, high=1.0, size=(datanum * ( env.n + 1),))
v = pyfm.FuzzyMeasureFitLPKinteractiveMaxChains(datanum, additive, env, K, dataset)
print( "datanum: ", datanum)
print( "additive: ", additive)
print( "K: ", K)
print( "dataset: ", dataset)
print( "v: ", v)

# Test wrapper for:
#    void py_FuzzyMeasureFitLPKinteractiveAutoK(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K, int* maxiters)
datanum = 10
additive = 2
K = 0.5
maxiters = 100
#dataset = [random.random()] * datanum * ( env.n + 1)
dataset = np.random.uniform(low=0.0, high=1.0, size=(datanum * ( env.n + 1),))
v = pyfm.FuzzyMeasureFitLPKinteractiveAutoK(datanum, additive, env, K, maxiters, dataset)
print( "datanum: ", datanum)
print( "additive: ", additive)
print( "K: ", K)
print( "maxiters: ", maxiters)
print( "dataset: ", dataset)
print( "v: ", v)

# Test wrapper for:
#    void py_FuzzyMeasureFitLPKinteractiveMarginal(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K, int submod)
datanum = 10
additive = 2
K = 0.5
submod = 1
dataset = np.random.uniform(low=0.0, high=1.0, size=(datanum * ( env.n + 1),))
v = pyfm.FuzzyMeasureFitLPKinteractiveMarginal(datanum, additive, env,  K, submod, dataset)
print( "datanum: ", datanum)
print( "additive: ", additive)
print( "submod: ", submod)
print( "K: ", K)
print( "dataset: ", dataset)
print( "v: ", v)

# Test wrapper for:
#    void py_FuzzyMeasureFitLPKinteractiveMarginalMaxChain(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K, int* maxiters, int submod)
datanum = 10
additive = 2
K = 0.5
submod = 1
dataset = np.random.uniform(low=0.0, high=1.0, size=(datanum * ( env.n + 1),))
v = pyfm.FuzzyMeasureFitLPKinteractiveMarginalMaxChain(datanum, additive, env, K, maxiters, submod, dataset)
print( "datanum: ", datanum)
print( "additive: ", additive)
print( "submod: ", submod)
print( "K: ", K)
print( "dataset: ", dataset)
print( "v: ", v)

# Test wrapper for:
#    void py_FuzzyMeasureFitLP(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)
datanum = 10
additive = 2
options = 0
indexlow = [0, 0, 0]
indexhihg = [1, 1, 1]
option1 = 0
orness = 0.5
dataset = np.random.uniform(low=0.0, high=1.0, size=(datanum * ( env.n + 1),))
v = pyfm.FuzzyMeasureFitLP(datanum, additive, env, options, indexlow, indexhihg, option1, orness, dataset)
print( "datanum: ", datanum)
print( "additive: ", additive)
print( "indexlow: ", indexlow)
print( "options: ", options)
print( "indexhihg: ", indexhihg)
print( "option1: ", option1)
print( "orness: ", orness)
print( "dataset: ", dataset)
print( "v: ", v)

# Test wrapper for:
#    void py_FuzzyMeasureFitLPMob(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)
datanum = 10
additive = 2
options = 0
indexlow = [0, 0, 0]
indexhihg = [1, 1, 1]
option1 = 0
orness = 0.5
dataset = np.random.uniform(low=0.0, high=1.0, size=(datanum * ( env.n + 1),))
Mob = pyfm.FuzzyMeasureFitLPMob(datanum, additive, env, options, indexlow, indexhihg, option1, orness, dataset)
print( "datanum: ", datanum)
print( "additive: ", additive)
print( "indexlow: ", indexlow)
print( "options: ", options)
print( "indexhihg: ", indexhihg)
print( "option1: ", option1)
print( "orness: ", orness)
print( "dataset: ", dataset)
print( "Mob: ", Mob)

# Test wrapper for:
#    void py_fittingOWA(int datanum, struct fm_env* env, double* out_v, double* dataset)
# documented, no example
datanum = 10
dataset = np.random.uniform(low=0.0, high=1.0, size=(datanum * ( env.n + 1),))
v = pyfm.fittingOWA(datanum, env, dataset)
print( "datanum: ", datanum)
print( "dataset: ", dataset)
print( "v: ", v)

# Test wrapper for:
#    void py_fittingWAM(int datanum, struct fm_env* env, double* out_v, double* dataset)
# documented, no example
datanum = 10
atanum = 10
dataset = np.random.uniform(low=0.0, high=1.0, size=(datanum * ( env.n + 1),))
v = pyfm.fittingWAM(datanum, env, dataset)
print( "datanum: ", datanum)
print( "dataset: ", dataset)
print( "v: ", v)



pyfm.fm_free( env)
n = 3
env = pyfm.fm_init( n)

# Test wrapper for:
#    void py_Interaction(double* Mob, double* out_v, struct fm_env* env)
Mob = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
v = pyfm.Interaction(Mob, env)
print( "Mob: ", Mob)
print( "v: ", v)

# Test wrapper for:
#    void py_InteractionB(double* Mob, double* out_v, struct fm_env* env)
Mob = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
v = pyfm.InteractionB(Mob, env)
print( "Mob: ", Mob)
print( "v: ", v)

# Test wrapper for:
#    void py_InteractionMob(double* Mob, double* out_v, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
v = pyfm.InteractionMob(Mob, env)
print( "Mob: ", Mob)
print( "v: ", v)

# Test wrapper for:
#    void py_InteractionBMob(double* Mob, double* out_v, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
v = pyfm.InteractionBMob(Mob, env)
print( "Mob: ", Mob)
print( "v: ", v)


# Test wrapper for:
#    void py_BipartitionShapleyIndex(double* v, double* out_w, struct fm_env* env)
# not documented in R or Python user guide
v = [0.0, 0.3, 0.5, -0.2, 0.4, 0.1]
s = pyfm.BipartitionShapleyIndex(v, env)
print( "v: ", v)
print( "s: ", s)

# Test wrapper for:
#    void py_BipartitionBanzhafIndex(double* v, double* out_w, struct fm_env* env)
# not documented in R or Python user guide
v = [0.0, 0.3, 0.5, -0.2, 0.4, 0.1]
s = pyfm.BipartitionBanzhafIndex(v, env)
print( "v: ", v)
print( "s: ", s)

# Test wrapper for:
#    void py_NonadditivityIndexMob(double* Mob, double* out_w, struct fm_env* env)
# not documented in R or Python user guide
Mob = [0.2, 0.3, 0.5, -0.2, 0.4, 0.1]
s = pyfm.NonadditivityIndexMob(Mob, env)
print( "v: ", v)
print( "s: ", s)

# Test wrapper for:
#    void py_NonadditivityIndex(double* v, double* out_w, struct fm_env* env)
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
w = pyfm.NonadditivityIndex(v, env)
print( "v: ", v)
print( "w: ", w)

# Test wrapper for:
#    void py_NonmodularityIndex(double* v, double* out_w, struct fm_env* env)
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
w = pyfm.NonmodularityIndex(v, env)
print( "v: ", v)
print( "w: ", w)

# Test wrapper for:
#    void py_NonmodularityIndexMob(double* Mob, double* out_w, struct fm_env* env)
v =[0.0, 0.3, 0.5, -0.2, 0.4, 0.1, -0.2, 0.1]
w = pyfm.NonmodularityIndexMob(v, env)
print( "v: ", v)
print( "w: ", w)

# Test wrapper for:
#    void py_NonmodularityIndexMobkadditive(double* Mob, double* out_w, int k,  struct fm_env* env)
k = 2
Mob =[0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
pnm = pyfm.NonmodularityIndexMobkadditive(Mob, k, env)
print( "k: ", k)
print( "Mob: ", Mob)
print( "nonmodularity indices: ", pnm)

# Test wrapper for:
#    int py_IsMeasureBalanced(double* v, struct fm_env* env)
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
is_measure = pyfm.IsMeasureBalanced(v, env)
print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    int py_IsMeasureSelfdual(double* v, struct fm_env* env)
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
is_measure = pyfm.IsMeasureSelfdual(v, env)
print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    int py_IsMeasureSubadditive(double* v, struct fm_env* env)
v = [0.0, 0.3, 0.5, -0.2, 0.4, 0.1, -0.2, 0.1]
is_measure = pyfm.IsMeasureSubadditive(v, env)
print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    int py_IsMeasureSubmodular(double* v, struct fm_env* env)
v = [0.0, 0.3, 0.5, -0.2, 0.4, 0.1, -0.2, 0.1]
is_measure = pyfm.IsMeasureSubmodular(v, env)
print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    int py_IsMeasureSuperadditive(double* v, struct fm_env* env)
v = [0.0, 0.3, 0.5, -0.2, 0.4, 0.1, -0.2, 0.1]
is_measure = pyfm.IsMeasureSuperadditive(v, env)
print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    int py_IsMeasureSymmetric(double* v, struct fm_env* env)
v = [0.0, 0.3, 0.5, -0.2, 0.4, 0.1, -0.2, 0.1]
is_measure = pyfm.IsMeasureSymmetric(v, env)

print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    int py_IsMeasureKMaxitive(double* v, struct fm_env* env)
v = [0.0, 0.3, 0.5, -0.2, 0.4, 0.1, -0.2, 0.1]
is_measure = pyfm.IsMeasureKMaxitive(v, env)
print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    int py_IsMeasureAdditiveMob(double* Mob, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
is_measure = pyfm.IsMeasureAdditiveMob(Mob, env)
print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    int py_IsMeasureBalancedMob(double* Mob, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
is_measure = pyfm.IsMeasureBalancedMob(Mob, env)
print( "v: ", v)
print( "is_measure: ", is_measure)


# Test wrapper for:
#    int py_IsMeasureSelfdualMob(double* Mob, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
is_measure = pyfm.IsMeasureSelfdualMob(Mob, env)
print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    int py_IsMeasureSubadditiveMob(double* Mob, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
is_measure = pyfm.IsMeasureSubadditiveMob(Mob, env)
print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    int py_IsMeasureSubmodularMob(double* Mob, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
is_measure = pyfm.IsMeasureSubmodularMob(Mob, env)
print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    int py_IsMeasureSuperadditiveMob(double* Mob, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
is_measure = pyfm.IsMeasureSuperadditiveMob(Mob, env)
print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    int py_IsMeasureSupermodularMob(double* Mob, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
is_measure = pyfm.IsMeasureSupermodularMob(Mob, env)
print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    int py_IsMeasureSymmetricMob(double* Mob, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
is_measure = pyfm.IsMeasureSymmetricMob(Mob, env)
print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    int py_IsMeasureKMaxitiveMob(double* Mob, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
is_measure = pyfm.IsMeasureKMaxitiveMob(Mob, env)
print( "v: ", v)
print( "is_measure: ", is_measure)

# Test wrapper for:
#    void py_Mobius(double* v, double* out_MobVal, struct fm_env* env)
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
Mob = pyfm.Mobius(v, env)
print( "v: ", v)
print( "Mob: ", Mob)

# Test wrapper for:
#    double py_OWA(double* x, double* v, struct fm_env* env)
# not documented in R or Python user guide
x = [0.3, 0.4, 0.8, 0.2]   # inputs
w = [0.4, 0.35 ,0.2 ,0.05] # OWA weights
res = pyfm.OWA(x, v, env)
print( "v: ", v)
print( "w: ", w)
print( "res: ", res)

# Test wrapper for:
#    double py_WAM(double* x, double* v, struct fm_env* env)
# not documented in R or Python user guide
x = [0.3, 0.4, 0.8, 0.2]   # inputs
w = [0.4, 0.35 ,0.2 ,0.05] # OWA weights
res = pyfm.WAM(x, v, env)
print( "v: ", v)
print( "w: ", w)
print( "res: ", res)

# Test wrapper for:
#    void py_Zeta(double* Mob, double* out_v, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
v = pyfm.Zeta(Mob, env)
print( "Mob: ", Mob)
print( "v: ", v)

# Test wrapper for:
#    void py_dualMobKadd(int k, double* src, double* out_dest, struct fm_env* env)
Mob = [0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
kadd = 2
dual, length = pyfm.dualMobKadd(kadd, Mob, env)
print( "Mob: ", Mob)
print( "kadd: ", kadd)
print( "length of output: ", length)
print( "dual: ", dual)

# Test wrapper for:
#    void py_Shapley2addMob(double* v, double* out_x, int n)
v = [0.0, 0.3, 0.5, -0.2, 0.4, 0.1]
n = len( v)
shapley = pyfm.Shapley2addMob( v, n)
print( "v: ", v)
print( "n: ", n)
print( "shapley: ", shapley)

# Test wrapper for:
#    void py_Banzhaf2addMob(double* v, double* out_x, int n)
v = [0.0, 0.3, 0.5, -0.2, 0.4, 0.1]
n = len(v)
banzhaf = pyfm.Banzhaf2addMob(v, n)
print( "v: ", v)
print( "n: ", n)
print( "banzhaf: ", banzhaf)

# Test wrapper for:
#    double py_Choquet2addMob(double* x, double* Mob, int n)
x =[0.2,0.5,0.4]
Mob = [0.2, 0.3, 0.5, -0.2, 0.4, 0.1]
n = len( Mob)
ci = pyfm.Choquet2addMob(x, Mob, n)
print( "x: ", x)
print( "Mob: ", Mob)
print( "CI: ", ci)

# Test wrapper for:
#    int py_fm_arraysize(int n, int kint, struct fm_env* env)
kint = 2
n = env.n
l = pyfm.fm_arraysize(n, kint, env)
print( "kint: ", kint)
print( "n: ", n)
print( "length: ", l)

# Test wrapper for:
#    int py_generate_fm_minplus(int num, int n, int kint, int markov, int option, double K, double* out_vv, struct fm_env* env)
# pyfm.generate_fm_minplus(num, n, kint, markov, option, K, out_vv, env)
# not documented in R or Python user guide
num = 10
n = 6
kint = 3
markov = 1000
option = 0
K = 0.7
ret_code = 0
length = 0
vv = []
ret_code, vv, length = pyfm.generate_fm_minplus(num, n, kint, markov, option, K, env)
print( "num: ", num)
print( "n: ", n)
print( "kint: ", kint)
print( "markov: ", markov)
print( "option: ", option)
print( "K: ", K)
print( "ret_code: ", ret_code)
print( "length of output: ", length)
print( "vv: ", vv)

# Test wrapper for:
#    int py_generate_fm_2additive_convex(int num, int n,  double* out_vv)
# not documented in R or Python user guide
num = 10
n = 6
ret_code = 0
length = 0
ret_code, vv, length = pyfm.generate_fm_2additive_convex(num, n)
print( "num: ", num)
print( "n: ", n)
print( "ret_code: ", ret_code)
print( "length of output: ", length)
print( "vv: ", vv)

# Test wrapper for:
#    int py_generate_fm_2additive_convex_withsomeindependent(int num, int n, double* out_vv)
# 
# not documented in R or Python user guide
num = 10
n = 6
ret_code = 0
length = 0
ret_code, vv, length = pyfm.generate_fm_2additive_convex_withsomeindependent(num, n)
print( "num: ", num)
print( "n: ", n)
print( "ret_code: ", ret_code)
print( "length of output: ", length)
print( "vv: ", vv)

pyfm.fm_free( env);
n = 3
env = pyfm.fm_init( n)

#
# --- Here the testing for env_sparse, n = 3 starts ---
# 

# Test wrapper for:
#    void py_prepare_fm_sparse(int n, int tupsize, int* tuples, struct fm_env_sparse* out_env)
n = 3
tupsize = 0
env_sparse = pyfm.prepare_fm_sparse( n, tupsize)

# Test wrapper for:
#    void py_add_tuple_sparse(int tupsize, int* tuple, double v, struct fm_env_sparse* env)
v = 0.2
tuple = [1, 2, 3]
pyfm.add_tuple_sparse( tuple, v, env_sparse)
print( "tuple: ", tuple)

# Test wrapper for:
#    void py_ShapleyMob_sparse(double* out_v, int n, struct fm_env_sparse* env)
n = 3
v = pyfm.ShapleyMob_sparse(n, env_sparse)
print( "n: ", n)
print( "Shapley values: ", v)

# Test wrapper for:
#    void py_BanzhafMob_sparse(double* out_v, int n, struct fm_env_sparse* env)
n = 3
v = pyfm.BanzhafMob_sparse(n, env_sparse)
print( "n: ", n)
print( "Banzhaf values: ", v)

# Test wrapper for:
#    void py_add_pair_sparse(int i, int j, double v, struct fm_env_sparse* env)
v = 0.2
i = 2
j = 3
pyfm.add_pair_sparse(i, j, v, env_sparse)
print( "v: ", v)
print( "i: ", i)
print( "j: ", j)


# Test wrapper for:
#    void py_populate_fm_2add_sparse_from2add(int n, double* v, struct fm_env_sparse* env)
n = 3
yy, v, length = pyfm.generate_fm_2additive_convex_withsomeindependent( 1, n) 
print( "n: ", n)
print( "v: ", v)
pyfm.populate_fm_2add_sparse_from2add( n, v, env_sparse)

# Test wrapper for:
#    void py_populate_fm_2add_sparse(double* singletons, int numpairs, double* pairs, int* indicesp1, int* indicesp2, struct fm_env_sparse* env)
numpairs = 3
singletons = [0.1,0.2,0.3]
pairs = [0.4,0.5,0.6]
indicesp1 = [1,1,2]
indicesp2 = [2,3,3]
pyfm.populate_fm_2add_sparse(singletons, numpairs, pairs, indicesp1, indicesp2, env_sparse)
print( "numpairs: ", numpairs)
print( "singletons: ", singletons)
print( "pairs: ", pairs)
print( "indicesp1: ", indicesp1)
print( "indicesp2: ", indicesp2)

# Test wrapper for:
#    void py_expand_2add_full(double* out_v, struct fm_env_sparse* env)
n = 3
v = pyfm.expand_2add_full( n, env_sparse)
print( "n: ", n)
print( "v: ", v)

# Test wrapper for:
#    void py_sparse_get_singletons(int n, double* out_v, struct fm_env_sparse* env)
n = 3
v = pyfm.sparse_get_singletons(n, env_sparse)
print( "n: ", n)
print( "singletons: ", v)

# Test wrapper for:
#    int py_sparse_get_pairs(int* pairs, double* v, struct fm_env_sparse* env)
n = 3
pairs, v = pyfm.sparse_get_pairs( n, env_sparse)
print( "n: ", n)
print( "pairs: ", pairs)
print( "v: ", v)

# Test wrapper for:
#    int py_sparse_get_tuples(int* tuples, double* v, struct fm_env_sparse* env)
tuples, v = pyfm.sparse_get_tuples( env_sparse)
print( "tuples: ", tuples)
print( "v: ", v)

# Test wrapper for:
#    void py_Nonmodularityindex_sparse(double* out_w, int n, struct fm_env_sparse* env)
n =3
w = pyfm.Nonmodularityindex_sparse(n, env_sparse)
print( "n: ", n)
print( "w: ", w)

# Test wrapper for:
#    int py_tuple_cardinality_sparse(int i, struct fm_env_sparse* env)
i = 0;
tup_card = pyfm.tuple_cardinality_sparse(i, env_sparse)
print( "i: ", i)
print( "tup_card: ", tup_card)

# Test wrapper for:
#    int py_get_num_tuples(struct fm_env_sparse* env)
num_tup = pyfm.get_num_tuples(env_sparse)
print( "num_tup: ", num_tup)

# Test wrapper for:
#    int py_get_sizearray_tuples(struct fm_env_sparse* env)
length = pyfm.get_sizearray_tuples(env_sparse)
print( "length of array of tuples: ", length)

# Test wrapper for:
#    int py_is_inset_sparse(int A, int card, int i, struct fm_env_sparse* env)
A = 0
card = 3
i = 1
is_contained = pyfm.is_inset_sparse(A, card, i, env_sparse)
print( "A: ", A)
print( "card: ", card)
print( "i: ", i)
print( "is_contained: ", is_contained)

# Test wrapper for:
#    int py_is_subset_sparse(int A, int cardA, int B, int cardB, struct fm_env_sparse* env)
A = 0
cardA = 3
B = 1
cardB = 2
is_subset = pyfm.is_subset_sparse(A, cardA, B, cardB, env_sparse)
print( "A: ", A)
print( "cardA: ", cardA)
print( "B: ", B)
print( "cardB: ", cardB)
print( "is_subset: ", is_subset)

# Test wrapper for:
#    double py_min_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env)
x = [0.1,0.05,0.2]
n = 3
S = 0
cardS = 3
yy = pyfm.min_subset_sparse(x, n, S, cardS, env_sparse)
print( "x: ", x)
print( "n: ", n)
print( "S: ", S)
print( "cardS: ", cardS)
print( "yy: ", yy)

# Test wrapper for:
#    double py_max_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env)
x = [0.1,0.05,0.2]
n = 3
S = 0
cardS = 3
yy =pyfm.max_subset_sparse(x, n, S, cardS, env_sparse)
print( "x: ", x)
print( "n: ", n)
print( "S: ", S)
print( "cardS: ", cardS)
print( "yy: ", yy)

# Test wrapper for:
#    double py_ChoquetMob_sparse(double* x, int n, struct fm_env_sparse* env)
x = [0.1,0.05,0.2]
c_i = pyfm.ChoquetMob_sparse(x, env_sparse)
print( "x: ", x)
print( "Choquet integral: ", c_i)

# Test wrapper for:
#    void py_free_fm_sparse( struct fm_env_sparse* env)
pyfm.free_fm_sparse( env_sparse)
pyfm.fm_free(env)

#
# --- new env sparse for n = 5 ---
#
n = 5
tupsize = 0
env_sparse = pyfm.prepare_fm_sparse( n, tupsize)

# Test wrapper for:
#    int   py_generate_fm_2additive_convex_sparse(int n, struct fm_env_sparse* env)
yy = pyfm.generate_fm_2additive_convex_sparse(n, env_sparse)
print( "n: ", n)
print( "yy: ", yy)

# Test wrapper for:
#    int   py_generate_fm_kadditive_convex_sparse(int n, int k, int nonzero, struct fm_env_sparse* env)
k = 4
nonzero = 10
yy = pyfm.generate_fm_kadditive_convex_sparse(n, k, nonzero, env_sparse)
print( "n: ", n)
print( "k: ", k)
print( "nonzero: ", nonzero)
print( "yy: ", yy)

#
# --- free env sparse for n = 5 ---
#
pyfm.free_fm_sparse( env_sparse)



############# FUNCTIONS VERSION 5 #######

#New Functions Pytmtools 5
fm=pyfm
#alias

#fm.generate_fm_2additive(num, n)
num=3
n=5
ret_code, v, len = fm.generate_fm_2additive(num, n)
print(v)
print(ret_code)
print(len)

#fm.CheckMonMob2additive2(v, n)
ret_code, v, len =fm.generate_fm_2additive(1, 10)
n=10
check = fm.CheckMonMob2additive2(v, n)
print(check)


#fm.generate_fm_2additive_randomwalk2(num, n, markov, option, step, Fn)
num=2
n=5
ret_code, v, len = fm.generate_fm_2additive_randomwalk2(num, n, 1000, 0, 0.001, None)
print(v)
print(ret_code)
print(len)

#fm.generate_fm_sorting(num, n, markov, option, env)
env=fm.fm_init(3)
markovsteps=100
fuzzymeasures = fm.generate_fm_sorting(num, 3, markovsteps, 0, env)
print(fuzzymeasures)

#fm.generate_fm_balanced(num, n, env)
#env=fm.fm_init(3)
ret_code, v, len = fm.generate_fm_balanced(num, 3, env)
print(v)
print(ret_code)
print(len)

#fm.generateAntibuoyant(n, env)
#env=fm.fm_init(3)
antibuoyant = fm.generateAntibuoyant(3, env)
print(antibuoyant)

#fm.generate_fm_randomwalk(num, n, kadd, markov, option, step, env, Fn)
def Fn(n, v):
   out = 0.0
   for i in range(n[0]):
     out += v[i]
   #print(out,n[0],v[1])
   if out > 1:
      return 0
   else:
      return 1
#env=fm.fm_init(3)
step=0.0010
Option=3
n=3
ret_code, v,len= fm.generate_fm_randomwalk(num, n, 2, 10, Option, step, env, Fn)
print(v)
print(ret_code)
print(len)

#fm.CheckMonotonicitySortMerge(n, v, env)
#env=fm.fm_init(3)
n=3
v=fm.generate_fm_sorting(1, 3, 1000, 0, env)
print(v)
ret_code, index = fm.CheckMonotonicitySortMerge(n, v, env)

print(ret_code)
#print(index)

#fm.CheckMonotonicitySortInsert(v, indices, env)

n=3
# already initialised above
#env=fm.fm_init(n)
v=fm.generate_fm_sorting(1, n, 1000, 0, env)
ret_code, index=fm.CheckMonotonicitySortMerge(n, v, env)
v[1] *= 1.1
ret_code, index=fm.CheckMonotonicitySortInsert(n, v, index, env)

print(ret_code)
#print(index)

#fm.CheckMonotonicitySimple(v, env)

#env=fm.fm_init(3)
v=fm.generate_fm_sorting(1, 3, 1000, 0, env)
monotonicity=fm.CheckMonotonicitySimple(v, env)

print(monotonicity)

#fm.CheckMonotonicityMob(Mob, len, env)

#env=fm.fm_init(3)
step=0.001
Fn=None
Option=3
ret_code, Mob, len = fm.generate_fm_randomwalk(1, 3, 2, 1000, Option, step, env, Fn)
print(len)
check=fm.CheckMonotonicityMob(Mob, len, env)
print(Mob)
print(check)


#fm.CheckConvexityMonMob(Mob, len, env)
#env=fm.fm_init(3)
step=0.001
Fn=None
Option=5
#5 means convex kadditive
ret_code, Mob, len = fm.generate_fm_randomwalk(1, 3, 2, 1000, Option, step, env, Fn)

check=fm.CheckConvexityMonMob(Mob, len, env)
print(Mob)
print(check)

fm.fm_free(env)

#fm.generate_fm_kinteractivedualconvex(num, n, kadd, markov,  step, env, Fn)
n=4
env=fm.fm_init(n)
step=0.001
Fn=None
ret_code, Mob, len = fm.generate_fm_kinteractivedualconvex(num, n, 2, 1000, step, env, Fn)
print(Mob)
print(ret_code)
print(len)

#fm.generate_fm_kinteractivedualconcave(num, n, kadd, markov,  step, env, Fn)
#env=fm.fm_init(3)
step=0.001
Fn=None
ret_code, Mob, len = fm.generate_fm_kinteractivedualconcave(num, n, 2, 1000, step, env, Fn)
print(Mob)
print(ret_code)
print(len)




#fm.ConvertCoMob2KinterCall(n, kadd, len, Mob, fullmu, env)

n=4
env=fm.fm_init(n)
num=1
fullmu=0
step= 0.001
Fn=None
ret_code, Mob, len = fm.generate_fm_kinteractivedualconvex(num, n, 2, 1000,  step, env, Fn)
print(Mob,len)
v=fm.ConvertCoMob2Kinter(n, 2, len, Mob, fullmu, env)
print(v)
v=fm.ConvertCoMob2Kinter(n, 2, len, Mob, 1, env)
print(v)
#fm.ChoquetCoMobKInter(x, Mob, kadd, len, env)

#env=fm.fm_init(3)
step= 0.001
Fn=None
ret_code, Mob, len= fm.generate_fm_kinteractivedualconvex(1, n, 2, 1000,  step, env, Fn)
x=[0.2,0.5,0.4,0.1]
print(Mob,len)
ChoquetCoMobKInter=fm.ChoquetCoMobKInter(x, Mob, 2, len, env)
print(ChoquetCoMobKInter)

fm.fm_free(env)



#fm.FuzzyMeasureFit2Additive(num, n, options, indexlow, indexhigh, option1, orness, data)
#env=fm.fm_init(3)
num=20
n=3
d = np.array([0.00125122, 0.563568, 0.193298, 0.164338,
            0.808716, 0.584991, 0.479858, 0.544309,
            0.350281, 0.895935, 0.822815, 0.625868,
            0.746582, 0.174103, 0.858917, 0.480347,
            0.71048, 0.513519, 0.303986, 0.387631,
            0.0149841, 0.0914001, 0.364441, 0.134229,
            0.147308, 0.165894, 0.988495, 0.388044,
            0.445679, 0.11908, 0.00466919, 0.0897714,
            0.00891113, 0.377869, 0.531647, 0.258585,
            0.571167, 0.601746, 0.607147, 0.589803,
            0.166229, 0.663025, 0.450775, 0.357412,
            0.352112, 0.0570374, 0.607666, 0.270228,
            0.783295, 0.802582, 0.519867, 0.583348,
            0.301941, 0.875946, 0.726654, 0.562174,
            0.955872, 0.92569, 0.539337, 0.633631,
            0.142334, 0.462067, 0.235321, 0.228419,
            0.862213, 0.209595, 0.779633, 0.498077,
            0.843628, 0.996765, 0.999664, 0.930197,
            0.611481, 0.92426, 0.266205, 0.334666,
            0.297272, 0.840118, 0.0237427, 0.168081]).reshape(num, 4)
indexlow=[0.1,0.1,0.2]
indexhigh=[0.9,0.9,0.5]
options=3
option1=1
orness=[0.1,0.7]
v = fm.FuzzyMeasureFit2Additive(num, 3, options, indexlow, indexhigh, option1, orness, d)
print(v)

fm.fm_free(env)
