#pragma once
/*

These  functions generate random fuzzy measures (general or k-interactive) by the MiimalsPlus and topologial sort methods
followed by Markov chain.

They are based on generating linear extensions of partial orders. Each linear extension corresponds to a simplex in the polytope of fuzzy measures.
Then selecting a random point within a simplex results in a random point within the order polytope (uniformly distributed)

In addition, the functions may keep track of the linear extensions generated and then can print their distributions and also
calculates the distance from the uniform.

The method is based on randomisation and topological sorting as the initialisation step, followed by a few Markov chain steps.


Gleb Beliakov, April 2020


The functions take parameters:  (num m  kint Markovsteps option  K   vv)

num is the number of linear extensions to generate
m is the number of criteria so that 2^m is the size of the fuzzy measure (or size of the binary lattice Bn)

kint - (<= m) is the number k in k-interactive fuzzy measures. For example kint=1 means the measure is (almost) additive
(only singletons are free parameters, and there are m! linear extensions).

markovsteps - number of Markov chain steps to make. Start from 100 then 1000, 5000, ... the more is steps the beter quality
is the distribution but the more time the algorithm works.

option - not used for minimalsplus, but for topological sort , if 1 (but it is overwritten to 0 if the number of entries to sort * num is too large)
   then the Markov chain is also followed by a selection process which looks at the history of generated linear extensions (stored in a map with the help of hash keys),
   and choosing the orders which have not been used a large number of times. It uses reservoir sampling and favours less frequently used extensions to compensate
   for potential nonuniformity. For large m, kint (m>5) topological sort results in non-repeated extensions anyway, so this selection is not needed. hence set option =0
   Only for small m it may be set to 1.

K - parameter for the k-interactive fuzzy measures from (0,1]

Output: vv matrix of suze fmsize x num, with num rows, where the reandom fuzzy measure values are stored.
		The type myfloat needs to be defined as float or double in this file
		The fmsize is found by calling function fm_arraysize( m, 2^m,  kint)
		The fuzzy measures are arranged in cardinality based ordering with the last m-kint values corresponding to the cardinalities kint+1,...m
		the first element is always 0 (v(emptyset))

The function generate_fm_tsort is based on the topological sort of randomised entries of the partial order graph, followed by Markov chain and optionally
reservoir sampling to discourage repeating linear extensions.

The method is outlined in the paper by Beliakov, Cabrerizo, Herrera-Viedma and Wu "Random generation of k-interactive capacities"
currently under review.


The generate_fm_minplus is based on the minimalsPlus method, which
 is based on the program supplied by Elias Combarro and Susana Irene Diaz Rodribuez in October 2019,
which is also published in their paper

"Minimals plus: An improved algorithm for the random generation of linear extensions of partially ordered sets." Information
Sciences, 501:50-67, 2019.

The code can be optimised by not using the matrix representation of the poset, relying on the relation preceeds.Not attempted here due to lack of time.

The function generate_fm_tsort is faster than generate_fm_minplus based on our experiments. It requires less markov steps for convergence to uniform

Compiling:
	while the files binarylattice.cpp and minimalsplus.cpp are automatically included, the library fuzzymeasuretools.cpp has to be compiled separately and linked


Usage:

		m=5; kint=3;
		int_64 n ;

		Preparations_FM(m, &n); // to initialise some global variables. the probram will crash otherwise
		int arraysize = fm_arraysize(m, n, kint);

		myfloat* VV = new myfloat[arraysize*total];

		int option =1;

		myfloat K = 0.1;
		// use either one of the. tsort generally is faster
//		generate_fm_minplus(total, m, kint, Markov, option, K, VV);
		generate_fm_tsort(total,  m,  kint,  Markov,  option,  K, VV);

		//(CARDINALITY ordering!)
		// print the resulting fuzzy measures
		for (int i = 0;i < total;i++) {
			for (int j = 0;j < arraysize;j++)
				cout << VV[i*arraysize + j] << " ";
			cout << endl;
		}


Email me if there are any questions. It is a freeware.

Gleb Beliakov, April 2020
gleb@deakin.edu.au

*/

// These definitions can be changed to support other data types
//#include "fuzzymeasuretools.h"


typedef struct {
	double val;
	int_64 ind;
} dobint;

typedef struct {
	double val;
	int_64 ind;
} doblongint;




LIBDLL_API int fm_arraysize(int n, int_64 m, int kint);
// calculates the size of the array to store one k-interctive fuzzy measure in cardinality ordering
LIBDLL_API int fm_arraysize_kadd(int n, int k);
// same for k-additive in cardinality ordering

LIBDLL_API int fm_arraysize_2add(int n); 
// same for 2-additive and without 0

// generate fuzzy measures randomly using topological sort
LIBDLL_API int generate_fm_tsort(int_64 num, int n, int kint, int markov, int option, myfloat K, myfloat * vv);

// generate convex (supermodular)  fuzzy measures randomly using topological sort
LIBDLL_API int generate_fmconvex_tsort(int_64 num, int n, int kint, int markov, int option, myfloat K, myfloat * vv);

// generate fuzzy measures randomly using MinimalsPlus method
LIBDLL_API int generate_fm_minplus(int_64 num, int n, int kint, int markov, int option, myfloat K, myfloat * vv);

// generate simple 2 additive supermodular (convex) and submodular capacities
// size is the returned size of each vector in compact representation (singletons and pairs only
LIBDLL_API int generate_fm_2additive_convex(int_64 num, int n, int * size, myfloat * vv);

LIBDLL_API int generate_fm_2additive_concave(int_64 num, int n, int * size, myfloat * vv);

LIBDLL_API int generate_fm_2additive_convex_withsomeindependent(int_64 num, int n, int * size, myfloat * vv);
// as above, but resets randomly some interactions to 0

LIBDLL_API void export_maximal_chains(int n, int_64 m, double * v, double * mc);

LIBDLL_API int generate_fm_sorting01(int_64 num, int n, int markov, int option, double* vv);

LIBDLL_API int generate_fm_randomwalk(int_64 num, int n, int kadd, int markov, int option, double step , double* vv, int* len, void* extrachecks);

	//	option==0 normal, 1 convex, 2 antibuoyant, 3 kadditive  ,   4 belief,  5 kadditive convex , 
//option =0x0100 standars slower mon/convexiy check, 0x1000 or 0x0010 - avoid belief meaures to start walk 
//on the borders of the simplex



LIBDLL_API int CheckMonotonicitySortMerge(double* v, int_64* indices, int_64 m, int n);
LIBDLL_API int CheckMonotonicitySortInsert(double* v, int_64* indices, int_64 m, int n);
LIBDLL_API int CheckMonotonicitySimple(double* v, int_64 m, int n);


LIBDLL_API int CheckConvexitySortMerge(vector<doblongint>& v, vector<int_64>& indices, int_64 m, int n, int_64 M, int conv );
LIBDLL_API int CheckConvexitySortInsert(vector<doblongint>& v, vector<int_64>& indices, int_64 m, int n, int_64 M, int conv );
LIBDLL_API  int GenerateAntibuoyant(int n, int_64 m, double* out); // lambda
LIBDLL_API int generate_fm_simple_randomwalk(int_64 num, int n, int markov, int option, double noise, double* vv, int* len, void* extrachecks);
LIBDLL_API int generate_fm_convex_randomwalk(int_64 num, int n, int markov, int option, double noise, double* vv, int* len, void* extrachecks);


LIBDLL_API int CheckMonotonicityMob(double* Mob, int n, int_64 m, int_64 len);
LIBDLL_API int CheckConvexityMonMob(double* Mob, int n, int_64 m, int_64 len);

//LIBDLL_API int generate_fm_kadditive_randomwalk(int_64 num, int n, int kadd, int markov, int option, double noise, double* vv, void* extrachecks);
//LIBDLL_API int generate_fm_kadditiveconvex_randomwalk(int_64 num, int n, int kadd, int markov, int option, double noise, double* vv, void* extrachecks);
LIBDLL_API int generate_fm_belief(int_64 num, int n, int kadd, int_64* length, double* vv);
LIBDLL_API int generate_fm_balanced(int_64 num, int n, double* vv);

LIBDLL_API int generate_fm_kinteractivedualconvex(int_64 num, int n, int kadd, int markov, int_64* length, double noise, double* vv, void* extrachecks);
LIBDLL_API int generate_fm_kinteractivedualconcave(int_64 num, int n, int kadd, int markov, int_64* length, double noise, double* vv, void* extrachecks);

// 2 additive
LIBDLL_API int generate_fm_2additive(int_64 num, int n, int option, myfloat* vv);
LIBDLL_API int generate_fm_2additive_randomwalk2(int_64 num, int n, int markov, int option, double noise, double* vv, void* extrachecks);
LIBDLL_API  int CheckMonMob2additive2(double* Mob, int n, int length, double* temp);

LIBDLL_API void ConvertCoMob2Kinter(double* mu, double* Mob, int n, int_64 m, int kadd, int len, int fullmu);
LIBDLL_API double ChoquetCoMobKInter(double* x, double* Mob, int n, int_64 m, int kadd, int length);
