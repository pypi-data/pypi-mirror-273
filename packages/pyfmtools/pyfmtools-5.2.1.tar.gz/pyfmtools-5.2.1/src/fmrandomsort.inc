//LIBDLL_API int generate_fm_tsort(int_64 num, int n, int kint, int markov, int option, myfloat K, myfloat* vv);


#include<numeric>
#include <cmath>
#include<set>



typedef int (*USER_FUNCTION)(int*, double*);
const double Meps = 1e-20;

typedef vector<int> iVec;			//type define iVec to hold integer vector 
typedef vector<double> dVec;		//and dVec to hold double vectors.

void DoMarkovChainSimple(vector<int_64>& v, int k)
{
#ifndef NO_R
	unif_R_class<int_64> uni(0, (int)v.size() - 2);
#else	
	uniform_int_distribution<int_64> uni(0, (int)v.size() - 2); // guaranteed unbiased
#endif
	//uniform_int_distribution<int_64> uni(1, (int)v.size() - 2); // guaranteed unbiased

	for (int j = 0; j < k; j++)
	{
		//if(coin(rng))
		{
			int_64 pos = uni(rng);
			if (!IsSubset(v[pos + 1], v[pos]))
				std::swap(v[pos], v[pos + 1]);
		}
	}
}

void GenerateOnSimplex1(vector<double>& w, int_64 dim)
{
	for (int_64 i = 0; i < dim - 1; i++) w[i] = distribution(rng);
	sort(w.begin(), w.begin() + dim - 1, less<double>());
	w[dim - 1] = 1;
	for (int_64 i = dim - 1; i > 0; i--) w[i] = w[i] - w[i - 1];
}

double* valuesptr;
int fm_sortvals(size_t i1, size_t i2)
{return (valuesptr[i1] < valuesptr[i2]); }

// generate random fuzzy measures from 0-1 measures using sorting methods
LIBDLL_API int generate_fm_sorting01(int_64 num, int n, int markov, int option,  myfloat* vv)
{
	int_64 m = 0x1ULL << n;
	int MaxV = n + 5, MaxAntichain = n + 4;
	vector<int_64> Vertices(MaxV * MaxAntichain);
	vector<int> VertexLen(MaxV);
	vector<double> weights(MaxV);
	vector<double> values(m);
	vector<int_64> subsets(m);

	vector<int> perm(n);		iota(perm.begin(), perm.end(), 0);
	vector<int_64> bitswapped(m);	iota(bitswapped.begin(), bitswapped.end(), 0);

#ifndef NO_R
	unif_R_class<int_64> RanUG(1, (m - 2));
	unif_R_class<int> RanLen(1, MaxAntichain);
	unif_R_class<int> RanVertex(2, MaxV);
#else	
	uniform_int_distribution<int_64> RanUG(1, m - 2);  // choose unanimity game
	uniform_int_distribution<int> RanLen(1, MaxAntichain); // vertex composition
	uniform_int_distribution<int> RanVertex(2, MaxV);   //  number of vertices
#endif



	for (int_64 k = 0; k < num; k++) {     // generate num fuzzy measures
		  shuffle(perm.begin(), perm.end(), rng);// random permutation
          for (int_64 A = 0; A < m; ++A) bitswapped[A] = swapbits(A, perm, n); 

		  // Step 1. 
			int V = RanVertex(rng);   // we use V vertices here
			for (int i = 0; i < V * MaxAntichain; i++) Vertices[i] = RanUG(rng);
			for (int i = 0; i < V; i++) VertexLen[i] = RanLen(rng); 
			          // vertices of random compositions
			iota(subsets.begin(), subsets.end(), 0); // assign values 0,1,2,3,\ldots
			GenerateOnSimplex1(weights, V);    // V weights that sum to one
			for (int_64 A = 1; A < m - 1; A++) {    // for each subset of N
				values[A] = 0;
				for (int v = 0; v < V; v++) {
					int flag = 0;
					for (int ug = 0; ug < VertexLen[v]; ug++)
						if (IsSubset(A, Vertices[ug + v * V])) flag = 1;  // mu(A)=1
					if (flag) values[A] += weights[v];  // convex combination of vertices
				}
			}
			values[0] = 0;	values[m - 1] = 1; // empty set and N
   
   
            valuesptr=values.data();
			//sort(subsets.begin(), subsets.end(), [&values](size_t i1, size_t i2) {return (values[i1] < values[i2]); });
   
   
            sort(subsets.begin(), subsets.end(),fm_sortvals);
 // sort keeping track of changing positions of elements
				 // Now the subsets is reordered according to LE and we generate a fuzzy measure
				 // improvements symmeterise and MC
			DoMarkovChainSimple(subsets, markov); // just a few Markov chain steps are enough
			for (int A = 0; A < m; ++A) subsets[A] = bitswapped[subsets[A]]; 

				 // Step 2.
			 values[0] = -0.1; values[m - 1] = 1.1;  // recycle values and safety before sorting
			 for (int_64 i = 1; i < m - 1; i++) 	values[i] = distribution(rng);
			 sort(values.begin(), values.end(), less<double>());  // ordered random vals
				     // assign to measure based on LE computed 
			 values[0] = 0; values[m - 1] = 1;  
			 for (int_64 A = 0; A < m; A++) vv[subsets[A] + k*m ] = values[A]; 
			     // now use, save or print this fuzzy measure
				
	} // end for loop
	return 1;
}



LIBDLL_API int generate_fm_2additive(int_64 num, int n, int option, myfloat* vv)
{   // simply take convex combination of all vertices
	//option==1 means starting with 1 (include emptyset in the output), otherwise not , start with 0
	int length = fm_arraysize_2add(n) ;
	vector<double> w(length);
	vector<double> values(length);
	// take 0 or not? for now without 0
	for (int k = 0; k < num; k++)
	{
		GenerateOnSimplex1(w, length);
		// decide on =ve and -ve by random flip
		for (int i = 0; i < n; i++)
			values[i] = w[i];
		int u = n;
		for (int i = 0; i < n - 1; i++)
			for (int j = i + 1; j < n; j++)
			{
				double r = distribution(rng);
				if (r < 0.5) {
					values[u] = -w[u];
					values[i] += w[u];
					values[j] += w[u];
				}
				else {
					values[u] = w[u];
				}
				u++;
			}

		// here decide if include 0 or not
		if (option == 1) {
			for (int_64 A = 0; A < length; A++) vv[1 + A + k * (length + 1)] = values[A];
			vv[k * (length + 1)] = 0;
		}
		else
			for (int_64 A = 0; A < length; A++) vv[A + k * length] = values[A];
	}
	return (length + option); //returns the length of each FM

}



int fm_random_sort_flag = 0;

struct lesser {

	bool operator()(const dobint& a, const dobint& b) const
	{
		if (a.val < b.val && IsSubset(a.ind, b.ind)) fm_random_sort_flag = 1;    // conraditions
		if (a.val > b.val && IsSubset(b.ind, a.ind)) fm_random_sort_flag = 1;
		return a.val < b.val;
	}
};

typedef unsigned int uint;

LIBDLL_API int CheckMonotonicitySortMerge(vector<dobint>& v, int_64 m, int n)
{
	// m= 2^n, therefore there are m/2 pairs and n -1 levels to merge
	   // check each pair
	for (int_64 i = 0; i < m; i += 2)
		if (v[i].val > v[i + 1].val) return 0;// these should be sorted

	vector<dobint> aux(m);
	fm_random_sort_flag = 0;

	int_64 i = 2; // pairs
	while (i <= m / 2) {
		for ( int_64 j = 0; j <= m - i * 2; j += i * 2) {
			merge(&(v[j]), &(v[j + i]), &(v[j + i]), &(v[j + 2 * i]), &(aux[j]), lesser());
			if (fm_random_sort_flag) return 0;
		}
		i *= 2;

		if (i >= m) {
			//copy aux to v and return 1
			copy(aux.begin(), aux.end(), v.begin());
			return 1; // all sorted
		}
		for (  int_64 j = 0; j <= m - i * 2; j += i * 2) {
			merge(&(aux[j]), &(aux[j + i]), &(aux[j + i]), &(aux[j + 2 * i]), &(v[j]), lesser());
			if (fm_random_sort_flag) return 0;
		}
		i *= 2;
	}
	return 1; // all done in v
}


LIBDLL_API int CheckMonotonicitySortInsert(vector<dobint>& v, int_64 m, int n)
{
	// assume v is almost sorted and is almost an LE
	for (  int_64 i = 1; i < m; i++)
	{
		dobint key = v[i];
		long long int j = i - 1;
		while (j >= 0 && v[j].val > key.val) {
			if (IsSubset(key.ind, v[j].ind)) return 0;  // key smaller but the subset larger
			v[j + 1] = v[j];
			j--;
		}
		v[j + 1] = key;
	}
	return 1; // all is fine
}


LIBDLL_API int CheckMonotonicitySimple(vector<dobint>& v, int_64 m, int n)
{
	for (int_64 A = 1; A < m - 1; A++)
	{
		int_64 B;
		for (int i = 0; i < n; i++)
			if (!IsInSet(A, i)) {
				B = A;
				AddToSet(&B, i);
				if (v[A].val > v[B].val) {  return 0; }
			}
	}
	return 1;
}


LIBDLL_API int CheckMonotonicitySortMerge(double* v, int_64* indices, int_64 m, int n)
{
	vector<dobint> vv(m);
	for (int_64 i = 0; i < m; i++) { vv[i].val = v[i]; vv[i].ind = indices[i]; }
	int res= CheckMonotonicitySortMerge(vv, m, n);
	for (int_64 i = 0; i < m; i++) { v[i] = vv[i].val; indices[i]= vv[i].ind ; }
	return res;
}
LIBDLL_API int CheckMonotonicitySortInsert(double* v, int_64* indices, int_64 m, int n)
{
	vector<dobint> vv(m);
	for (int_64 i = 0; i < m; i++) { vv[i].val = v[i]; vv[i].ind = indices[i]; }
	int res = CheckMonotonicitySortInsert(vv,m,n);
	for (int_64 i = 0; i < m; i++) { v[i] = vv[i].val; indices[i] = vv[i].ind; }
	return res;
}
LIBDLL_API int CheckMonotonicitySimple(double* v, int_64 m, int n)
{
	for (int_64 A = 1; A < m - 1; A++)
	{
		int_64 B;
		for (int i = 0; i < n; i++)
			if (!IsInSet(A, i)) {
				B = A;
				AddToSet(&B, i);
				if (v[A] > v[B]) { return 0; }
			}
	}
	return 1;
}










const int_64 mask1 = 0xFF00000000000000;
const int_64 mask2 = 0x00FFFFFFFFFFFFFF;

const int shift1 = 56;


int fm_random_sort_flagConv = 0;


bool ConditionAntibuouyant(int_64 A, int_64 B) // returns 1 if NOT OK 0 if OK
{// (i not=j, B subset A, i in B)
	return(((A & mask1) != (B & mask1)) && IsSubset(A & mask2, B & mask2) && IsInSet(A & mask2, (B >> shift1) & (0xFF)));
}


bool ConditionConv(int_64 A, int_64 B) // returns 1 if NOT OK 0 if OK
{// A<B means i is the same and A subset B
	return(((A & mask1) == (B & mask1)) && IsSubset(A & mask2, B & mask2));
}

struct lesserConv {

	bool operator()(const doblongint& a, const doblongint& b) const
	{
		if (a.val < b.val && ConditionConv(a.ind, b.ind)) fm_random_sort_flagConv = 1;    // contradictions
		if (a.val > b.val && ConditionConv(b.ind, a.ind)) fm_random_sort_flagConv = 1;
		return a.val < b.val;
	}
};


struct lesserAntiBuoyant {

	bool operator()(const doblongint& a, const doblongint& b) const
	{
		if (a.val < b.val && ConditionAntibuouyant(a.ind, b.ind)) fm_random_sort_flagConv = 1;    // contradictions
		if (a.val > b.val && ConditionAntibuouyant(b.ind, a.ind)) fm_random_sort_flagConv = 1;
		return a.val < b.val;
	}
};






void PerturbVector( vector<dobint>& mymeasure, int_64 m, int n, double noise)
{
	for (int_64 i = 1; i < m-1; i++) // leave the ends
	{
		mymeasure[i].val +=  noise * (distribution(rng) - 0.5) ;
	}
}


void PerturbVector(vector<double>& v, vector<double>& v1, int_64 m, int n, double noise)
{
	for (int_64 i = 1; i < m-1; i++) // leave the ends
	{
		v1[i] = v[i] + noise * (distribution(rng) - 0.5) ;
	}
}


void PerturbVectorMob(vector<double>& v, vector<double>& v1, int_64 m, int n, double noise)
{
	GenerateOnSimplex1(v1, m - 1);
	double r = 1.0 / (m - 1);
	for (int_64 i = 0; i < m - 1; i++) v1[i] -= r;

	for (int_64 i = m-1; i > 0 ; i--) // leave the start 0
	{
		v1[i] = v[i] + noise * v1[i-1];
	}
	v1[0] = 0; // keep that one 0
}

void PerturbVectorMobWith0(vector<double>& v, vector<double>& v1, int_64 m, int n, double noise)
{

	GenerateOnSimplex1(v1, m );
	double r = 1.0 / (m );
	for (int_64 i = 0; i < m ; i++) v1[i] -= r;
//	cout << "P" << endl;
	for (int_64 i=0 ; i  < m ; i++) 
	{
		v1[i] = v[i] + noise * v1[i];
	}
//	cout << "P" << endl;
	//v1[0] = 0; // keep that one 0
}


int_64 BuildDerivativesVector(vector<doblongint>& w, vector<int_64>& indices, int_64& m1, vector<double>& v, int_64 m, int n) // here m1 is n 2^n-1

//int BuildDerivativesVector(vector<doblongint> &w, unordered_map<int_64, int_64>  &indices, int_64& m1, vector<double> &v, int_64 m, int n) // here m1 is n 2^n-1
{
	// we need to record indices for perturbations, map would be OK but too large, array will do?? too large?
	m1 = (m * n) / 2;
	w.resize(m1);
	//	indices.clear();

	int_64 k = 0;
	for (int_64 A = 0; A < m; A++) {
		for (int i = 0; i < n; i++) {
			if (!IsInSet(A, i)) {
				int_64 B = A;
				int_64 idx = 0;
				AddToSet(&B, i);
				w[k].val = v[B] - v[A];
				idx = i; idx = idx << shift1;  idx &= mask1; idx |= A;
				//				cout << idx << endl;
				w[k].ind = idx;
				indices[A * n + i] = k;
				//indices[idx] = k;
				k++;
			}
		}
	}
	return k;
}

void printindices(vector<int_64>& indices, int_64& m1,  int_64 m, int n)
{
	int_64 k;
	for (int_64 A = 0; A < m; A++) {
		for (int i = 0; i < n; i++) {
			if (!IsInSet(A, i)) {
				int_64 B = A;
				int_64 idx = 0;
				AddToSet(&B, i);
				// now what is k?? k=indices[idx];

				idx = i; idx = idx << shift1; idx &= mask1; idx |= A;
				//k = indices[idx];
				k = indices[A * n + i];
//				cout << A << " " << i << " " << k << " " <<  " ";
			}
		}
	}
}

int PerturbDerivativesVector(vector<doblongint>& w, vector<int_64>& indices, int_64& m1, vector<double>& v, int_64 m, int n) // here m1 is n 2^n-1
//int PerturbDerivativesVector(vector<doblongint> &w, unordered_map<int_64, int_64> &indices, int_64& m1, vector<double> &v, int_64 m, int n) // here m1 is n 2^n-1
{
	// we need to record indices for
	int retflag = 1;
	m1 = (m * n) / 2;
	w.resize(m1);
	int_64 k = 0;
	for (int_64 A = 0; A < m; A++) {
		for (int i = 0; i < n; i++) {
			if (!IsInSet(A, i)) {
				int_64 B = A;
				int_64 idx = 0;
				AddToSet(&B, i);
				// now what is k?? k=indices[idx];

				idx = i; idx = idx << shift1; idx &= mask1; idx |= A;
				//k = indices[idx];
				k = indices[A * n + i];
				w[k].val = v[B] - v[A];
				w[k].ind = idx;
				if (w[k].val < -1e-20) retflag= 0; // non-positive, no monotonicity, but do not exit yet
			}
		}
	}

	return retflag; // all OK
}


int CheckConvexitySortInsertPartial(doblongint* start, int_64 n, int conv) // length n
{// conv==1 jusy convex else antibuoyant
	// assume v is almost sorted and is almost an LE
	fm_random_sort_flagConv = 0;
	for (int_64 i = 1; i < n; i++)
	{
		doblongint key = start[i];
		long long int j = i - 1;
		while (j >= 0 && start[j].val > key.val) {
			if (conv)
			{
				if (ConditionConv(key.ind, start[j].ind)) return 0;
			}
			else {
				if (ConditionAntibuouyant(key.ind, start[j].ind)) return 0;
			}
			//if (IsSubset(key.ind, v[j].ind)) return 0;  // key smaller but the subset larger
			start[j + 1] = start[j];
			j--;
		}
		start[j + 1] = key;
	}
	return 1; // all is fine
}

int numberofderivatives(int_64 A, int n) {
	return n - bitweight(A & mask2);
}
template< class BidirIt1, class BidirIt2 > void mycopy(BidirIt1 first, BidirIt1 last, BidirIt2 d_first) {
	while (first != last)
	{
		*d_first = *first;
		first++; d_first++;
	}
}

LIBDLL_API int CheckConvexitySortMerge(vector<doblongint>& v, vector<int_64>& indices, int_64 m, int n, int_64 M, int conv=1) // here m is n 2^n-1
//int CheckConvexitySortMerge(vector<doblongint> &v, unordered_map<int_64, int_64> &indices, int_64 m, int n) // here m is n 2^n-1
{
	// m= n 2^n-1, therefore there subarrays of length n to do by insertion sort and then merge
	// conv==1 convexity
	fm_random_sort_flagConv = 0;
	vector<int_64> positions, positions1;
	positions.push_back(0);
	for (int_64 i = 0; i < m;) {
		int_64 num = numberofderivatives(v[i].ind, n);
		positions.push_back(num + i);
		if (CheckConvexitySortInsertPartial(&(v[i]), num, conv) == 0) return 0;
		i += num;
	}
	//	positions.push_back(m); // just in case

	vector<doblongint> aux(m);
	fm_random_sort_flagConv = 0;

	// here m is not power of 2 ??????
	//int_64 i = n; // n tuples
	while (positions[1] < m) {
		//	for (unsigned int j = 0;j <= m - i * 2; j += i * 2) 
		int r=0;
		positions1.push_back(0);
		//vector< doblongint>::iterator it, it1;
		vector<int_64>::iterator pos, pos1;
		pos = positions.begin();

		do {
			//int_64 num= numberofderivatives(v[j].ind);

			pos1 = pos + 1;
			if (pos1 != positions.end() && v.begin() + *pos1 < v.end())
				//if (positions.end() != pos1 + 1)
				if(conv) merge(v.begin() + *pos, v.begin() + *pos1, v.begin() + *pos1, v.begin() + *(pos1 + 1), aux.begin() + *pos, lesserConv());
					else merge(v.begin() + *pos, v.begin() + *pos1, v.begin() + *pos1, v.begin() + *(pos1 + 1), aux.begin() + *pos, lesserAntiBuoyant());
			else
				copy(v.begin() + *pos, v.end(), aux.begin() + *pos);

			if (fm_random_sort_flagConv) return 0;
			pos++;
			if (v.begin() + *pos < v.end()) pos++;
			positions1.push_back(*pos);

			/*
						if (positions[r + 2] <= m && positions[r + 1] <= m)  {
							if(positions[r + 1] < positions[r + 2])
								merge(&(v[positions[r]]), &(v[positions[r + 1]]), &(v[positions[r + 1]]), &(v[positions[r + 2]]), &(aux[positions[r]]), lesserConv());
							else {
								it = v.begin()+positions[r]; it1 = aux.begin()+positions[r];

								copy(it, v.end(), it1);
							}
							if (flagConv) return 0;
							positions1.push_back(positions[r + 2]);
							r += 2;
							*/

			if (*pos >= m) break;
		} while (1);
		//		positions1.push_back(m);

		positions.clear();


		if (positions1[1] >= m) {
			//copy aux to v and return 1
			copy(aux.begin(), aux.end(), v.begin());
			goto Lreindex; // all sorted
		}

		positions.push_back(0);
		r = 0;
		pos = positions1.begin();
		do {

			pos1 = pos + 1;
			if (pos1 != positions1.end() && aux.begin() + *pos1 < aux.end())
				//if (positions.end() != pos1 + 1)
				if(conv) merge(aux.begin() + *pos, aux.begin() + *pos1, aux.begin() + *pos1, aux.begin() + *(pos1 + 1), v.begin() + *pos, lesserConv());
				else merge(aux.begin() + *pos, aux.begin() + *pos1, aux.begin() + *pos1, aux.begin() + *(pos1 + 1), v.begin() + *pos, lesserAntiBuoyant());
			else
				copy(aux.begin() + *pos, aux.end(), v.begin() + *pos);

			if (fm_random_sort_flagConv) return 0;
			pos++;
			if (aux.begin() + *pos < aux.end()) pos++;
			positions.push_back(*pos);
			if (*pos >= m) break;

			/*/
						//int_64 num= numberofderivatives(v[j].ind);
						if (positions1[r + 2] <= m && positions1[r + 1] <= m ){
							if( positions1[r + 1] < positions1[r + 2])
								merge(&(aux[positions1[r]]), &(aux[positions1[r + 1]]), &(aux[positions1[r + 1]]), &(aux[positions1[r + 2]]), &(v[positions1[r]]), lesserConv());
							else {
								it = aux.begin() + positions1[r]; it1 = v.begin() + positions1[r];
								copy(it, aux.end(), it1);
							}
							if (flagConv) return 0;
							positions.push_back(positions1[r + 2]);
							r += 2;
						}
						else break;
						*/
		} while (1);

		//	positions.push_back(m);

		positions1.clear();
	}

Lreindex:
	for (int_64 i = 0; i < M; i++)
	{
		indices[(v[i].ind & mask2) * n + ((v[i].ind >> shift1) & (0xFF))] = i;
//		cout << i << " " << (v[i].ind & mask2) << " " << ((v[i].ind >> shift1) & (0xFF)) << " ";
		//indices[v[i].ind] = i;
	}
	return 1; // all done in v
}

LIBDLL_API int CheckConvexitySortInsert(vector<doblongint>& v, vector<int_64>& indices, int_64 m, int n, int_64 M, int conv=1) // here m is n 2^n-1
//int CheckConvexitySortInsert(vector<doblongint> &v, unordered_map<int_64, int_64> &indices, int_64 m, int n) // here m is n 2^n-1
{
	fm_random_sort_flagConv = 0;
	// assume v is almost sorted and is almost an LE
	for (int_64 i = 1; i < m; i++)
	{
		doblongint key = v[i];
		long long int j = i - 1;
		while (j >= 0 && v[j].val > key.val) {
			if (conv)
			{
				if (ConditionConv(key.ind, v[j].ind)) return 0;
			}
			else {
				if (ConditionAntibuouyant(key.ind, v[j].ind)) return 0;
			}
			//if (IsSubset(key.ind, v[j].ind)) return 0;  // key smaller but the subset larger
			v[j + 1] = v[j];
			j--;
		}
		v[j + 1] = key;
	}
			// reindex  (why not needed here?)
//	cout << endl << "after insert" << endl;
			for (int_64 i = 0; i < M; i++)
			{

				indices[(v[i].ind & mask2)*n + ((v[i].ind >> shift1)&(0xFF))] = i;
				//int t = (v[i].ind >> shift1) & (0xFF);
				//cout << i << " " << (v[i].ind & mask2) << " " << t << " ";
			}
			
	return 1; // all is fine
}



void GenerateBelief(int n, int_64 m, vector<double>& out)
{
	vector<double> bel(m);
	vector<double> bel1(m - 2);

	for (int i = 0; i < m - 2; i++)
		bel1[i] = (double)distribution(rng);

	sort(bel1.begin(), bel1.end(), less<double>());

	bel[0] = 0;
	bel[1] = bel1[0];
	for (int i = 1; i < m - 2; i++)
		bel[i + 1] = bel1[i] - bel1[i - 1];

	bel[m - 1] = 1.0 - bel1[m - 3];

	Zeta(&(bel[0]), &(out[0]), n, m);
}


void GenerateBeliefMob(int n, int_64 m, vector<double>& out)
{// no zero, start with singleton
	//vector<double> bel(m);
	vector<double> bel1(m - 1);

	for (int_64 i = 0; i < m - 1; i++)
		bel1[i] = (double)distribution(rng);

	sort(bel1.begin(), bel1.end(), less<double>());

	//out[0] = 0;
	out[0] = bel1[0];
	for (int_64 i = 1; i <= m - 2; i++)
		out[i + 0] = bel1[i] - bel1[i - 1];

	out[m - 1] = 1.0 - bel1[m - 2];
}


int TriesLimit = 10000;
extern double auxarray[];
extern int auxN;
extern double auxfun(double lam);
typedef double (*USER_FUNCTION_BIS)(double);
extern double bisection(double a, double b, USER_FUNCTION_BIS f, int nmax);


LIBDLL_API  int GenerateAntibuoyant(int n, int_64 m, double* out)
{
	vector<double> sing(n), sinv(n);
	double on = 1.0 / n;

	int tries = 0;

	while (1) {
		for (int i = 0; i < n; i++)
			sing[i] = (double)distribution(rng) * on;

		// find lambda
		double lambda;
		double tol = 1.0e-9;
		int i;
		auxN = n;
		double cond = 0;
		double a, b, c;

		for (i = 0; i < n; i++) { cond += sing[i]; auxarray[i] = sing[i]; }
		if (fabs(cond - 1) < tol) // additive
		{
			lambda = 0;
			c = 0;
			goto E1;
		}

		{ //means we have to use this interval
			a = tol;
			b = 1e8;
			c = bisection(a, b, auxfun, 100000);
		}
		// so lambda is c now
		lambda = c;
	E1:;

		for (int i = 0; i < n; i++) if (sing[i] > 1e-10)  sinv[i] = 1. / sing[i]; else sinv[i] = 1e10;

		int res = 1;

		// conditions
		for (int i = 0; i < n; i++)
			for (int j = 0; j < n; j++)
				if (fabs(sinv[i]- sinv[j]) > lambda  ) {
					res = 0;
					break;
				}
		if (res) {
			// OK
			ConstructLambdaMeasure(sing.data(), &c, out, n, m);
			return 1;
		}
		tries++;
		if (tries > TriesLimit) return 0;
	}
}









LIBDLL_API int generate_fm_simple_randomwalk(int_64 num, int n, int markov, int option, double noise, double* vv, int* len, void* extrachecks)
{
	//	option==0 normal, 1 convex, 2 antibuoyant, 3   ,   4 belief,  option & 0xF = sparse in Mob

	int_64 m = 0x1ULL << n;
	USER_FUNCTION FF = (USER_FUNCTION)extrachecks;
	int res,success = 0;

	vector<dobint> mymeasure(m);
	vector<dobint> mymeasure1(m);
	vector<double> values(m);

	for (int_64 k = 0; k < num; k++) {     // generate num fuzzy measures
		generate_fm_sorting01(1, n, 5, 0, values.data());

		for (int_64 A = 0; A < m; A++) {
			mymeasure[A].val = values[A];
			mymeasure[A].ind = (unsigned long int)A;
		}

		res = CheckMonotonicitySortMerge(mymeasure, m, n);
		// start walk
		for (int steps = 0; steps < markov; steps++) {
			PerturbVector(mymeasure, m, n, noise);
			
			res = CheckMonotonicitySortInsert(mymeasure, m, n);

			// here any extra checks
			if (res && extrachecks != NULL) {
				// cast and call
				// copy
				for (int_64 A = 0; A < m; A++) values[A] = mymeasure[A].val;
				int m1 = (int)m;
				res = FF(&m1, values.data());
			}

			if (res) { //OK
				// save it
				copy(mymeasure.begin(), mymeasure.end(), mymeasure1.begin());
				success++;
			}
			else { // one step back
				copy(mymeasure1.begin(), mymeasure1.end(), mymeasure.begin());
				fm_random_sort_flag = 0;
			}
		}

		
		for (int_64 A = 0; A < m; A++) vv[mymeasure[A].ind + k * m] = mymeasure[A].val;
		vv[0+k*m] = 0; vv[m - 1 +k*m] = 1; // for safety 
	}

	*len =(int) m;
	return success;
}


LIBDLL_API int generate_fm_convex_randomwalk(int_64 num, int n, int markov, int option, double noise, double* vv, int* len, void* extrachecks)
{
	int_64 m1, m = 0x1ULL << n;
	int success = 0;
	int r1;
	USER_FUNCTION FF = (USER_FUNCTION)extrachecks;
//	unordered_map<int_64, int_64>  indices, indicesTemp;

	vector<int_64> vindices, vindicesTemp;
	vector<double> v, v1;
	vector<doblongint> w, w1; // derivatives

	v.resize(m); v1.resize(m);
	vindices.resize(m * n);

	int res;
	int_64 M;
	for (int_64 k = 0; k < num; k++) {     // generate num fuzzy measures
		// take any convex FM
		GenerateBelief(n, m, v);

		if (markov == 0) {
			res = 1;
			if (res && extrachecks != NULL) {
				// cast and call
				int m1 = (int)m;
				res = FF(&m1, v.data());
			}
			if (res) goto L1; //save it
		}
		fm_random_sort_flagConv = 0;
		M=BuildDerivativesVector(w, vindices, m1, v, m, n); // M is the length of w
		r1 = CheckConvexitySortMerge(w, vindices, m1, n, M);

		if (r1) {
			for (int r = 0; r < markov; r++)
			{
				vindicesTemp = vindices; // to be modified during perturbations


				int res = 0;
				PerturbVector(v, v1, m, n, noise);

				res = PerturbDerivativesVector(w1, vindices, m1, v1, m, n); //vindicestemp
					//perturb
				if (res)
					res = CheckConvexitySortInsert(w1, vindices, m1, n, M); //vindicestemp for the output
							// here any extra checks
				if (res && extrachecks != NULL) {
					// cast and call
					int m1 = (int)m;
					res = FF(&m1, v1.data());
				}
				if (res)
				{
					// save
					copy(v1.begin(), v1.end(), v.begin());
					copy(vindices.begin(), vindices.end(), vindicesTemp.begin());

					success++;
				}
				else {
					// roll back
					//copy(v.begin(), v.end(), v1.begin());
					copy(vindicesTemp.begin(), vindicesTemp.end(), vindices.begin());
					fm_random_sort_flagConv = 0;
				}
			} //for markov

		}
		
		// we can do an extra check r1 = IsMeasureSupermodular(&(v[0]), m);
	L1:;
		for (int_64 A = 0; A < m; A++) vv[A + k * m] = v[A];
		vv[0 + k * m] = 0; vv[m - 1 + k * m] = 1; // for safety 
	}
	*len = (int)m;
	return success;
}



LIBDLL_API int generate_fm_antibuoyant_randomwalk(int_64 num, int n, int markov, int option, double noise, double* vv, int* len, void* extrachecks)
{
	int_64 m1, m = 0x1ULL << n;
	int success = 0;
	int r1;
	fm_random_sort_flagConv = 0;
	unordered_map<int_64, int_64>  indices, indicesTemp;
	USER_FUNCTION FF = (USER_FUNCTION)extrachecks;

	vector<int_64> vindices, vindicesTemp;
	vector<double> v, v1;
	vector<doblongint> w, w1;

	v.resize(m); v1.resize(m);
	vindices.resize(m * n);


	for (int_64 k = 0; k < num; k++) {     // generate num fuzzy measures
		// take any convex FM
		int r=GenerateAntibuoyant(n, m, v.data());
		if (!r) // something is wrong, cannot find one random lambda measure 
			return 0;

		int_64 M=BuildDerivativesVector(w, vindices, m1, v, m, n);
		r1 = CheckConvexitySortMerge(w, vindices, m1, n,  M, 0);

		if (r1) {
			for (int r = 0; r < markov; r++)
			{
				//indicesTemp = indices; // to be modified during perturbations
				vindicesTemp = vindices; // to be modified during perturbations

				int res = 0;
				PerturbVector(v, v1, m, n, noise);

				PerturbDerivativesVector(w1, vindices, m1, v1, m, n); //vindicestemp
					//perturb

				res = CheckConvexitySortInsert(w1, vindices, m1, n, M, 0); //vindicestemp for the output
							// here any extra checks
				if (res && extrachecks != NULL) {
					// cast and call
					int m1 = (int)m;
					res = FF(&m1, v1.data());
				}
				if (res)
				{
					// save
					copy(v1.begin(), v1.end(), v.begin());
					copy(vindices.begin(), vindices.end(), vindicesTemp.begin());
					success++;
				}
				else {
					// roll back
					copy(v.begin(), v.end(), v1.begin());
					copy(vindicesTemp.begin(), vindicesTemp.end(), vindices.begin());
					fm_random_sort_flagConv = 0;
				}
			} //for markov

		}

		for (int_64 A = 0; A < m; A++) vv[A + k * m] = v[A];
		vv[0 + k * m] = 0; vv[m - 1 + k * m] = 1; // for safety 
	}
	*len = (int)m;
	return success;
}



LIBDLL_API void ZetaKAdd(double* Mob, double* v, int n, int length, int_64 m)
//inverse Moebius transform, from a k additive measure to full
{
	int_64 i;
	int_64 id;
	double s;
	for (i = 0; i < m; i++) {
		s = 0;
		for (id = 0; id <length; id++) if (IsSubset(i, card2bit[id]  )) {
			s += Mob[id];
		}
		v[i] = s;
	}
}

LIBDLL_API int CheckMonotonicityMob(double* Mob,  int n, int_64 m, int_64 len)
{
	for (int i = 0; i < n; i++) {
		double s = 0;
		for (int_64 A = 1; A < m; A++) if(IsInSet(A,i) ) { // for all sets
			s=0;
			for (int_64 B = 1; B < len; B++) if( IsInSet(card2bit[B],i)  && IsSubset(A, card2bit[B]) )
				s+= Mob[B];
			if(s < -1e-100) return 0;
		}
	}
	return 1;
}

int CheckMonMobSubset(double* Mob, int_64 A, int n, int_64 m, int_64 len)
{
	for (int i = 0; i < n; i++) {
		double s = 0;
		if (IsInSet(A, i)) { // for all sets
			s = 0;
			for (int_64 B = 1; B < len; B++) if (IsInSet(card2bit[B], i) && IsSubset(A, card2bit[B]))
				s += Mob[B];
			if (s < -1e-100) return 0;
		}
	}
	return 1;
}
LIBDLL_API int CheckMonMobSmart(double* Mob, int n, int_64 m,  int_64 len)
{
//	int lengthpairs = fm_arraysize_2add(n); // just check

	for (int i = 1; i <= n; i++) if (Mob[i] < -1e-100) return 0; // all singletons need to be positive

	set<int_64> negatives;
	for (int i = n+1; i < len; i++) if (Mob[i] < -1e-100) negatives.insert(card2bit[i]); // all tuples

	for (int_64 A = 1; A < m; A++) {
		//check if A is set union of negatives
		int_64 C = A;
		for (auto& val : negatives) {
			if (IsSubset(A, val)) {
				C = Setdiff(C, val);
			}

			if (C == 0) // yes, union of val
			{
				if (!CheckMonMobSubset(Mob, A, n, m, len)) return 0;
				else break;
			}
		}
	}
	return 1;
}


int CheckConvexityMob(double* Mob, int n, int_64 m, int_64 len)
{
	for (int i = 0; i < n; i++) 
		for (int j = i+1; j < n; j++) 
	{
		int_64 C = 0; AddToSet(&C, i); AddToSet(&C, j);

		double s = 0;
		for (int_64 A = 1; A < m; A++) if (IsSubset(A, C) ) 
		{ // for all sets that have i,j
			s=Mob[bit2card[C]]; // always start from C, can go until card(A) or min(bit2card[A]+1,len) but usually len is smaller anyway
			for (int_64 B = bit2card[C]+1; B < len; B++) if (IsSubset(card2bit[B], C) && IsSubset(A, card2bit[B]))
				s += Mob[B];

			if (s < -1e-100) return 0;
		}
		
	}
	return 1;
}

int CheckConvexityMobSubset(double* Mob, int_64 A, int n, int_64 m, int_64 len)
{
	// as above for one particular subset A
	for (int i = 0; i < n; i++)
		for (int j = i + 1; j < n; j++)
		{
			int_64 C = 0; AddToSet(&C, i); AddToSet(&C, j);
			double s = 0;
			if (IsSubset(A, C))
			{ // for all sets that have i,j
				s = Mob[bit2card[C]]; // always start from C, can go until card(A) or min(bit2card[A]+1,len) but usually len is smaller anyway
				for (int_64 B = bit2card[C] + 1; B < len; B++) if (IsSubset(card2bit[B], C) && IsSubset(A, card2bit[B]))
					s += Mob[B];

				if (s < -1e-100) return 0;
			}

		}
	return 1;
}

LIBDLL_API int CheckConvexityMonMob(double* Mob, int n, int_64 m, int_64 len)
{
	for (int i = 0; i <= n; i++) if (Mob[i] < -1e-100) return 0;
	return CheckConvexityMob(Mob,n,m,len);
}


LIBDLL_API int CheckMonMobKinter(double* Mob, int n,  int_64 len)
{
	// check monotonicity for setsother than singletons

	int_64 B, A, N = UniversalSet(n);
	for (int i = 0; i < n; i++)
	{
		double s = 0;
		int_64 C = 0; AddToSet(&C, i);
		for (A = 0; A < len - n; A++) {
			s = 0;
			int_64 BA = Setdiff(N, card2bit[A]);
			if (IsSubset(BA, C))
				for (B = A; B < len - n; B++) {
					int_64 BB = Setdiff(N, card2bit[B]); // smaller set
					if (IsSubset(BB, C) && IsSubset(BA, BB)) {
//						cout << A << " " << BA << " " << B << " " << BB << " "<<Mob[B]<<endl;
						s += Mob[B];
//						cout << s << endl;
					}
				}
			// add respective singleton in normal ordering
			s += Mob[len - n  + i];
//			cout << "s " << s << " " << Mob[len - n  + i] << " " << len - n  + i << endl;
			if (s < -1e-100) return 0;
		}
	}
	return 1;
}

LIBDLL_API int CheckConvexityMonMobKinter(double* Mob, int n,  int_64 len, int concave)
{
//	for (int i = 0; i < len; i++) cout << Mob[i] << " ";
//	cout << endl;	
	
	for (int i = 0; i < n; i++) if (Mob[len-i-1] < -1e-100) return 0; // singletons, always positive
	int res = 1;


	if (concave) res= CheckMonMobKinter(Mob,n,len); // monotonicity needs to be checked

//	cout <<"mon " << res << endl;

	if (!res) return 0;// not monotone

	int_64 B,A, N = UniversalSet(n);
	for (int i = 0; i < n; i++)
		for (int j = i + 1; j < n; j++)
		{
			double s = 0;
			int_64 C = 0; AddToSet(&C, i); AddToSet(&C, j);
			for (A = 0; A < len - n; A++) { // for each A
				s = 0;
				int_64 BA = Setdiff(N, card2bit[A]);
				if(IsSubset(BA,C))
				for (B = A; B < len - n; B++) {
					int_64 BB = Setdiff(N, card2bit[B]); // smaller set
					if (IsSubset(BB,C) && IsSubset(BA, BB)) {
						s += Mob[B];
					//	cout << A << " " << BA << " " << BB << " " << C << " " << Mob[B] << " "<<s<<endl;
					}
				}
//				cout << s << " s" << endl;
				if (!concave && ( s < -1e-100)) return 0;
				if (concave && (s > 1e-100)) return 0;			
			}//A
		}

	return 1;
}




LIBDLL_API int CheckConvexityMonMobSmart(double* Mob, int n, int_64 m, int kadd, int_64 len)
{
	int lengthpairs = fm_arraysize_kadd(n, 2) ; // just check, includes 0
	for (int i = 0; i < lengthpairs; i++) if (Mob[i] < -1e-100) return 0; // all pairs need to be positive

	set<int_64> negatives;
	for (int i = lengthpairs; i < len; i++) if (Mob[i] < -1e-100) negatives.insert(card2bit[i]);

	for (int_64 A = 1; A < m; A++) {
		//check if A is set union of negatives
		int_64 C = A;
		for (auto& val : negatives) {
			if (IsSubset(A, val)) {
				C = Setdiff(C, val);
			}

			if (C == 0) // yes, union of val
			{
				if (!CheckConvexityMobSubset(Mob, A, n, m, len)) return 0;
				else break;
			}
		}
	}

/*
	vector<int_64> mapset;
	for (auto& val : negatives) mapset.push_back(val); // got an array
	int_64 T = mapset.size();
	// we assume that T is small, decide here if revert to  standard check
	if (T >= n - 1) return CheckConvexityMob(Mob,n,m,len);

	int_64 PT = 1ULL << T;
	// now I have the bit ordering of components of mapset, so go through all of its subsets

	set<int_64> setsdone;
	for (int_64 B = 1; B < PT; B++) {
		// check for set A
		int_64 A = 0;
		for(int i=0;i<T;i++) if(IsInSet(B,i)) A=Setunion(A, mapset[i]);
		if (setsdone.find(A)==setsdone.end()) {// A not there
			setsdone.insert(A);
			if (!CheckConvexityMobSubset(Mob, A, n, m, len)) return 0;
		}
	}
	*/

	return 1;
}



// in Mobius and in cardinality ordering
LIBDLL_API int generate_fm_belief(int_64 num, int n, int kadd, int_64* length,  double* vv)
{
	if (kadd < n - 1)
		*length = fm_arraysize_kadd(n, kadd);
	else *length = 0x1ULL << n; 

	vector<double> v1(*length);
	for (int_64 k = 0; k < num; k++) {
		GenerateBeliefMob(n, *length-1, v1); // in Mobius! with no 0
		
		vv[0+ (*length)*k] = 0;

		for (int i = 0; i < *length-1; i++)
			vv[i + 1 + (*length) * k] = v1[i]; // last one?
	}
	return 1;
}

LIBDLL_API int generate_fm_balanced(int_64 num, int n, double* vv)
{
	int_64 m = 1ULL << n;
	vector<double> borders(n);
	vector<double> v(m);

	for (int_64 k = 0; k < num; k++) {
		for (int i = 0; i < n - 2; i++) borders[i] = distribution(rng);
		borders[n - 2] = 1.0;
		if(n>2) sort(borders.begin(), borders.begin() + n - 2, less<double>());
		for (int_64 i = 1; i < m-1; i++)
		{
			int card = Cardinality(i);
			if (card == 1) v[i] = distribution(rng) * borders[card - 1];
			else
				v[i] = distribution(rng) * (borders[card -1]- borders[card - 2]) + borders[card-2];
		}
		vv[k * m + 0] = 0;
		vv[k * m + m-1] = 1;

		for (int_64 i = 1; i < m - 1; i++) vv[k * m + i] = v[i];
	}
	return 1;
}

double FunSqr(double  A, double B, double C, double x) {  return A / (x + B ) + C; }

void generate_starting_kinteractive(int n, int kadd, double* Mob, int length)
{
	double a = distribution(rng);
	//a = 1. / n * a + (1. - a) / (n - kadd - 1.); // a in that range
	
	a = 1. / n * a + (1. - a) / (n - kadd - 0.5); // a fix, a can be too large for the formula to work ??

	// we use formula for mu for the n-kadd,... n as mu=A/(k+B)+C + MUstart
	// the coefs are per formulas below using f(0)=0, f'(0)=a, f(k+1)=Delta

	// ordering cardinality by N-|A| up to n-k, and then n singletons on top

	int length1 = fm_arraysize_kadd(n, kadd);

	double b = 1. / (kadd + 1) * (1. - a * (n - kadd - 1));
	vector<double> MA; MA.reserve(n);
	for (int i = length1; i < length; i++) Mob[i] = a; // singletons
	// proceed backward
	int q = length1 - 1;

	double MUstart = a * (n - kadd - 1);
	double r = kadd + 1;
	double Delta = 1 - MUstart;

	double denom =a*r-Delta;

	double B = r*Delta / denom;
	double A =-B*B*a;
	double C = -A/B;



	double mu = MUstart+ FunSqr(A,B,C,1);

	MA.push_back(mu - a * (n - kadd));
	// fill
	int j = (int)choose(n - kadd, n);
	for (int i = 0; i < j; i++) Mob[q - i] = MA[0];
	q -= j;

//	cout << MUstart << " " << Delta << " " << A << " " << B <<" "<<C<< endl;

	for (int k = n - kadd + 1; k <= n; k++) {

		mu = MUstart + FunSqr(A,B,C, k - (n - kadd - 1));

	//	mu = a * (n - kadd - 1) + b * (k - (n - kadd - 1));
		j = (int)choose(k, n);
		// value

		double value = mu;// to subtract the sum
//		cout <<k<<" "<< mu << endl;

		for (int i = k - 1; i >= n - kadd; i--)
		{
			double t = (double)choose(i, k);
			value -= MA[i - (n - kadd)] * t;
			//			cout << "s " << i << " " << MA[i - (n - kadd)] * t << " " << MA[i - (n - kadd)]  << " "<<t<<endl;
		}
		value -= a * k; // singletons

		MA.push_back(value);
		for (int i = 0; i < j; i++)
			Mob[q - i] = value;

		q -= j;
	}
}


void generate_starting_kinteractive_old(int n, int kadd, double* Mob, int length)
{
	double a = distribution(rng);
	a = 1. / n * a + (1. - a) / (n - kadd - 1.); // a in that range
	// ordering cardinality by N-|A| up to n-k, and then n singletons on top

	int length1 = fm_arraysize_kadd(n, kadd);

	double b = 1. / (kadd + 1) * (1. - a * (n - kadd - 1));

	for (int i = length1; i < length; i++) Mob[i] = a; // singletons
	// proceed backward
	int q = length1 - 1;
	double  prevm, prevmu = a * (n - kadd - 1);
	for (int k = n - kadd; k <= n; k++) {
		int j = (int)choose(k, n);
		// value
		double mu = a * (n - kadd - 1) + b * (k - (n - kadd - 1));
		double value = mu;// -(k)*a;

		int m1 = -1;
		prevmu = mu - b;

		for (int r = k - 1; r >= 2; r--) {
			double t = (double)choose(r, k);

			t = t * m1 * prevmu;

			value += t;
			if (r >= n - kadd) prevmu -= b; else prevmu -= a;
			m1 *= -1;
		}
		if (IsOdd(k)) m1 = 1; else m1 = -1;
		value += m1 * k * a;

		for (int i = 0; i < j; i++)
			Mob[q - i] = value;

		// prevmu differs by b

		//...............
		prevm = value; prevmu = mu;
		q -= j;
	}
}
LIBDLL_API int generate_fm_kinteractivedualconvex(int_64 num, int n, int kadd, int markov, int_64* Length, double noise, double* vv, void* extrachecks)
{
	// start with convex
	//length will be as kadditive plus n singletons
	// we need a special way of operating with these for Choquet and others
	int length = fm_arraysize_kadd(n, kadd) +n;  // includes emptyset and extra singletons!
	*Length = length;
	vector<double> v1(length ), v2(length), vs(length );

	int res, success = 0;
	USER_FUNCTION FF = (USER_FUNCTION)extrachecks;

	// do walk, and checks in backward order, also monotonicity
	for (int_64 k = 0; k < num; k++) {
		generate_starting_kinteractive(n, kadd, vs.data(), length);

//		for(int i=0;i<length;i++) cout << vs[i] << " ";
//		cout << endl;

		for (int steps = 0; steps < markov; steps++) {
			PerturbVectorMobWith0(vs, v1, length, n, noise);

			res = CheckConvexityMonMobKinter(v1.data(), n, length, 1);

//			cout << res<< endl;
			if (res) {
				if (res && extrachecks != NULL) {
					// cast and call
					res = FF(&length, v1.data());
				}

				if (res) { //OK
					// save it
					copy(v1.begin(), v1.end(), vs.begin());
					success++;
				}
				
			}
			
		}
		for (int_64 A = 0; A < length; A++) vv[A + k * (length)] = vs[A];
	}

	return success;
}
LIBDLL_API int generate_fm_kinteractivedualconcave(int_64 num, int n, int kadd, int markov, int_64* Length,  double noise, double* vv, void* extrachecks)
{
	// easire case take belief 
	int length = fm_arraysize_kadd(n, kadd) + n;  // includes emptyset and extra singletons!
	*Length = length;
	int res,success=0;

	USER_FUNCTION FF = (USER_FUNCTION)extrachecks;

	vector<double> v1(length), v2(length), vs(length);
	

	// do walk, and checks in backward order, also monotonicity
	for (int_64 k = 0; k < num; k++) {
		GenerateOnSimplex1(vs, length);
		for (int steps = 0; steps < markov; steps++) {
			PerturbVectorMobWith0(vs, v1, length, n, noise);
			res = CheckConvexityMonMobKinter(v1.data(), n,  length, 0 );
			if (res) {
				if (res && extrachecks != NULL) {
					// cast and call
					res = FF(&length, v1.data());
				}

				if (res) { //OK
					// save it
					copy(v1.begin(), v1.end(), vs.begin());
					success++;
				}
			}

		}

		for (int_64 A = 0; A < length ; A++) vv[A + k * (length )] = vs[A];
	}

	return success;
}


double max_subsetComplementSign(double* x, int n, int_64 S)
{ // returns max x_i when i \in S, or 0 if S is empty
	int i,j=0;
	double r = -10e10;
	for (i = 0; i < n; i++) {
		if (!IsInSet(S, i)) { r = maxf(r, x[i]); j++; }
	}
	if (r < 0) r = 0;
    
	//if (IsOdd(j + 1)) r = -r; // Sign - no need, we take the Mob of the dual measure
// cout<<r<<" "<<S<<endl;
	return r;
}
LIBDLL_API double ChoquetCoMobKInter(double* x, double* Mob, int n, int_64 m, int kadd, int length)
/* This is an alternative calculation of the Choquet integral from the coMoebius transform for kinteractive FM.
*/
{
	double s = 0;
	
	int_64 A;// , N = UniversalSet(n);
	for (A = length - 1; A >= length - n; A--)  s += Mob[A] * x[length-A-1]; //singletons
 //cout<<s<<endl;
	for (A = 0; A < length - n; A++) {
		//int_64 B = Setdiff(N, card2bit[A]);

		//Bit2card(A, n, kadd, length - n);
		//if (IsOdd(bitweight(B) + 1)) t = -1; else t = 1;
		s +=  Mob[A] * max_subsetComplementSign(x, n, card2bit[A]);

		// should it be card2bit?????
	}
	return s;
}

LIBDLL_API void ConvertCoMob2Kinter(double* mu, double* Mob, int n, int_64 m, int kadd, int len, int fullmu)
// fullmu = 1 means 2^n entries binary order,  =0 compact k-interactive,cardinality ordering, but all singletons need to be the same, so only the first one is used
{
	int_64 A,B, N= UniversalSet(n);
	int Sz = fm_arraysize_kadd(n, kadd);
	mu[0] = 0;
	double s;
	switch (fullmu) {
	case 1: // full, mu has length 2^n
		for (A = 1; A < m; A++) {
			s = 0;
			for (B = 0; B < Sz; B++) {
				if (IsSubset(card2bit[B], A)) s += Mob[B];
			}
			B= Setdiff(N, A);
			for (int i = 0; i < n; i++)
				if (IsInSet(B, i)) s += Mob[Sz + i];// singletons

			mu[A] = 1 - s;
		}

		break;
	case 0: // cardinality order, compact
		len = Sz;
		for (A = 1; A < Sz; A++) {
			s = 0;
			for (B = 0; B < Sz; B++) {
				if (IsSubset(card2bit[B], card2bit[A])) s += Mob[B];
			}
			B = Setdiff(N, card2bit[A]);
			for (int i = 0; i < n; i++)
				if (IsInSet(B, i)) s += Mob[Sz +i];// singletons are all the same

			mu[A] = 1 - s;
		}
		// now the upper part
		for (int i = 0; i < n - kadd; i++) mu[i + Sz] = 1 - Mob[Sz] * (n-kadd -1 - i);//????? last singleton
		break;

	}
}

LIBDLL_API int generate_fm_kadditive_randomwalk(int_64 num, int n, int kadd, int markov, int option, double noise, double* vv, int* len, void* extrachecks)
{
	// option > 4 &0xF is whether to use convex on the border of beliefs
	// option &0xF == 1 use standard method 0 use sort
	int usestandard = ((option & 0xF)==1);
	int usesmart = (option & 0xF) == 4;
	if (usesmart) usestandard = 1;

	USER_FUNCTION FF = (USER_FUNCTION)extrachecks;

	int_64 m = 0x1ULL << n;
	int res, success = 0;

	vector<dobint> mymeasure(m);
	vector<dobint> mymeasure1(m);
	vector<double> values(m);
	fm_random_sort_flag = 0;

	int length = fm_arraysize_kadd(n, kadd) -1 ;  // excludes emptyset !
	int length1 = length + 1;
	vector<double> v1(length1), v2(length), vs(length1); 

	for (int_64 k = 0; k < num; k++) {     // generate num fuzzy measures
		GenerateBeliefMob(n, length, v1); // in Mobius! with no 0
		GenerateBeliefMob(n, length, v2);
		dualMobKadd(v2.data(), vs.data()+1, n,  length,  kadd);
		vs[0] = 0;
		double W=distribution(rng);
		// weighted average of 2 belief measures
		for (int i = 0; i < length; i++)
			vs[i + 1] = vs[i + 1] * (1.0 - W) + W * v1[i];

		// now vs starts form 0 up to length

		if (!usestandard) {
			// convert to full
			ZetaKAdd(vs.data(), values.data(), n, length + 1, m);
			v1[0] = 0;

			for (int_64 A = 0; A < m; A++) {
				mymeasure[A].val = values[A];
				mymeasure[A].ind = (unsigned long int)A;
			}

			res = CheckMonotonicitySortMerge(mymeasure, m, n);
		}
		// start walk
		for (int steps = 0; steps < markov; steps++) {
			PerturbVectorMob(vs, v1, length1, n, noise);
			v1[0] = 0;

			if (!usestandard) {
				ZetaKAdd(v1.data(), values.data(), n, length1, m);

				for (int_64 A = 0; A < m; A++) {
					mymeasure[A].val = values[mymeasure[A].ind];
					//				mymeasure[A].ind = (unsigned long int)A;
				}

				res = CheckMonotonicitySortInsert(mymeasure, m, n);
			}
			else if(usesmart) res = CheckMonMobSmart(v1.data(), n, m, length1); else
				res = CheckMonotonicityMob(v1.data(), n, m, length1);

			// here any extra checks
			if (res && extrachecks != NULL) {
				// cast and call
					res = FF(&length1, v1.data());
			}

			if (res) { //OK
				// save it
				copy(v1.begin(), v1.end(), vs.begin());
				success++;
			}
			else { // one step back
				fm_random_sort_flag = 0;
				//copy(mymeasure1.begin(), mymeasure1.end(), mymeasure.begin());
				// nothing, vs remains
			}
		}


		for (int_64 A = 0; A < length+1; A++) vv[A + k * (length+1)] = vs[A];
		//vv[0 + k * m] = 0; vv[m - 1 + k * m] = 1; // for safety 
	}
	*len = length+1;
	return success;
}



LIBDLL_API int generate_fm_kadditiveconvex_randomwalk(int_64 num, int n, int kadd, int markov, int option, double noise, double* vv, int*len, void* extrachecks)
{
	// as above but convex, hence check convexity, (and mon , der >=0), and start with belief
	// smart means we only consider the Mobius negative subsets and their unions
	int usestandard = (option & 0xF)==1;
	int usesmart = (option & 0xF) == 4;
	if (usesmart) usestandard = 1;
	int useborder = ((option >> 4) & 0xF) ==1;

	USER_FUNCTION FF = (USER_FUNCTION)extrachecks;

	int_64 m1,m = 0x1ULL << n;
	int res, success = 0;
	int r1;

	vector<int_64> vindices, vindicesTemp;

	vector<doblongint> w, w1; // derivatives
	vector<double> values;
	if (!usestandard) vindices.resize(m * n);
	if (!usestandard) vindicesTemp.resize(m * n);
	if (!usestandard) values.resize(m );

	int length = fm_arraysize_kadd(n, kadd) - 1;  // excludes emptyset !
	int lengthpairs = fm_arraysize_kadd(n, 2) - 1;

	int length1 = length + 1;
	fm_random_sort_flagConv = 0;

	*len = length1;

	vector<double> v1(length + 1),  vs(length + 1);
	int_64 M; 

	for (int_64 k = 0; k < num; k++) {     // generate num fuzzy measures

	Lrestart:;
		fill(v1.begin(), v1.end(), 0.0);
		if(useborder)
			GenerateBeliefMob(n, lengthpairs, v1); // in Mobius! with no 0, padded with 0
		else
			GenerateBeliefMob(n, length, v1); // in Mobius! with no 0
		vs[0] = 0;

		for (int i = 0; i < length; i++)
			vs[i + 1] = v1[i];


		if (kadd == 2) markov = 0;// automatically belief measure

		if (markov == 0) {
			res = 1;
			if (extrachecks != NULL) {
				// callback
				res = FF(&length1, vs.data());
			}
			if (res) goto L1; //save it
		}

		r1 = 1;
		// now vs starts form 0 up to length
		if (!usestandard) {
			// convert to full
			ZetaKAdd(vs.data(), values.data(), n, length + 1, m);
		
			M = BuildDerivativesVector(w, vindices, m1, values, m, n);

			r1 = CheckConvexitySortMerge(w, vindices, m1, n, M);
		} 

		if (r1) {
			for (int r = 0; r < markov; r++)
			{
				//indicesTemp = indices; // to be modified during perturbations
				//vindicesTemp = vindices; // to be modified during perturbations
				copy(vindices.begin(), vindices.end(), vindicesTemp.begin());
				PerturbVectorMob(vs, v1, length + 1, n, noise);
				
				if (!usestandard) {
					ZetaKAdd(v1.data(), values.data(), n, length + 1, m);

					res = PerturbDerivativesVector(w, vindices, m1, values, m, n); //vindicestemp
						//perturb
	
//					printindices(vindices, m1, m, n);
					if (res)
						res = CheckConvexitySortInsert(w, vindices, m1, n, M); //vindicestemp for the output

								// here any extra checks
					/*
					if (0) {
						res = CheckConvexityMonMob(v1.data(), n, m, length + 1);
						if (res) {
							cout << "contradition" << endl;
							for (int jj = 0; jj < length + 1; jj++) cout << v1[jj] << " ";
							cout << endl;
							res = 0;
							for (int jj = 0; jj < m; jj++) cout << values[jj] << " ";
							cout << endl;
							for (int jj = 0; jj < m1; jj++) cout << w1[jj].val << " "<<(w1[jj].ind & mask2) <<" " <<((w1[jj].ind >> shift1) & (0xFF))<<" ";
							cout << endl<<m1<<" "<<M<<endl;
							for (int jj = 0; jj < m1 - 1; jj++) if(ConditionConv(w1[jj].ind, w1[jj+1].ind)){
								cout<<jj<<" "<<(w1[jj].ind & mask2) << " " << ((w1[jj].ind >> shift1) & (0xFF)) << " " <<
									(w1[jj+1].ind & mask2) << " " << ((w1[jj+1].ind >> shift1) & (0xFF)) << " "<<endl;
							}
							return 0;
						}
					}
					*/
				}
				else { //standard Mobius check
					if(usesmart) res=CheckConvexityMonMobSmart(v1.data(), n, m, kadd, length + 1);
					else res = CheckConvexityMonMob(v1.data(), n, m, length + 1);
				}
				if (res && extrachecks != NULL) {
					// cast and call
					res = FF(&length1, v1.data());
				}
				
				if (res)
				{
					// save
					copy(v1.begin(), v1.end(), vs.begin());
					if (!usestandard) copy(vindices.begin(), vindices.end(), vindicesTemp.begin());
					success++;
				}
				else {
					// roll back
					// keep vs
					if (!usestandard) copy(vindicesTemp.begin(), vindicesTemp.end(), vindices.begin());
					fm_random_sort_flagConv = 0;
				}
			} //for markov

		}
		else {
			//cout << "starting not convex" << endl;
			goto Lrestart;
		}
		// we can do an extra check r1 = IsMeasureSupermodular(&(v[0]), m);
	L1:;
		for (int_64 A = 0; A < length+1; A++) vv[A + k * (length+1)] = vs[A];
	}

	return success;
}



LIBDLL_API int generate_fm_randomwalk(int_64 num, int n, int kadd, int markov, int option, double noise , double* vv, int* len, void* extrachecks)
{
	//	option==0 normal, 1 convex, 2 antibuoyant, 3 kadditive  ,   4 belief,  5 kadd convex,  option & 0xF = sparse in Mob
	// kadd matters only when option=3 or 5 some other kadd
	int res;
	int option1 = ((option >> 8) & 0xFF);
	option = option & 0xFF;

	switch (option ) {

	case 1: res=generate_fm_convex_randomwalk(num, n, markov, option1, noise, vv, len, extrachecks); break;
	case 2: res=generate_fm_antibuoyant_randomwalk(num, n, markov, option1, noise, vv, len, extrachecks); break;
	case 4: res=generate_fm_convex_randomwalk(num, n, 0, option1, noise, vv, len, extrachecks); break;
// sparse in Mob, k-additive

		// kadditive: length should be compted, because vv is in cardinality ordering and not full vector m
	case 3: res = generate_fm_kadditive_randomwalk(num, n, kadd, markov, option1, noise, vv, len, extrachecks); break;
	case 5: res = generate_fm_kadditiveconvex_randomwalk(num, n, kadd, markov, option1, noise, vv, len,extrachecks); break;

	case 0: 
	default:
		res=generate_fm_simple_randomwalk(num, n, markov, option,  noise, vv, len, extrachecks); break;
	}

	return res;

}


/*
void PerturbVectorMob1(vector<double>& v, vector<double>& v1, int_64 m, int n, double noise)
{
	GenerateOnSimplex1(v1, m);

	double r = 1.0 / (m);
	for (int i = 0; i < m; i++) v1[i] -= r;

	for (int i = m - 1; i >= 0; i--) // no  start 0
	{
		v1[i] = v[i] + noise * v1[i];
	}
}*/

LIBDLL_API  int CheckMonMob2additive2(double* Mob, int n, int length, double* temp)
{
	// simple method, length not used
	// check positivity of singletons
	for (int i = 0; i < n; i++) if (Mob[i] < -Meps || Mob[i]> 1 + Meps) return 0; else temp[i] = Mob[i];

	int k = n;
	for (int i = 0; i < n - 1; i++)
		for (int j = i + 1; j < n; j++) {
			// pair ij at position k
			if (Mob[k] > 1 + Meps) return 0;

			if (Mob[k] < 0) {
				if (Mob[k] < -1 - Meps) return 0; //
				temp[i] += Mob[k];
				temp[j] += Mob[k]; // subtract
			}
			k++;
		}
	for (int i = 0; i < n; i++) if (temp[i] < -Meps) return 0;

	return 1;
}
void PerturbVectorMob1(vector<double>& v, vector<double>& v1, int_64 m, int n, double noise)
{
	GenerateOnSimplex1(v1, m);

	double r = 1.0 / (m);
	for (int i = 0; i < m; i++) v1[i] -= r;

	for (int i = m - 1; i >= 0; i--) // no  start 0
	{
		v1[i] = v[i] + noise * v1[i];
	}
}
LIBDLL_API int generate_fm_2additive_randomwalk2(int_64 num, int n, int markov, int option, double noise, double* vv, void* extrachecks)
{
	// the proposed simple set of inequalities
	//int_64 m = 0x1ULL << n;
	int res, success = 0;
	fm_random_sort_flag = 0;

	int length = fm_arraysize_2add(n);

	USER_FUNCTION FF=(USER_FUNCTION) extrachecks;

	/*	vector<int_64> Card2Bit2add(length);

		int k = 0;
		for (int i = 0; i < n; i++) Card2Bit2add[i] = (1ULL < i); // singletons
		k = n;
		for (int i = 0; i < n - 1; i++)
			for (int j = i + 1; j < n; j++) {
				int_64 B = (1ULL < i);
				B |= (1ULL < j);
				Card2Bit2add[k] = B;
				k++;
			}
			*/
	dVec v1(length ), v2(length ), vs(length );

	dVec aux1(length+1);


	for (int_64 k = 0; k < num; k++) {     // generate num fuzzy measures

		generate_fm_2additive(1, n, 0, vs.data());

/*		GenerateBeliefMob2(n, length - 1, v1); // in Mobius! with no 0
		GenerateBeliefMob2(n, length - 1, v2);
		dualMobKadd(v2.data(), vs.data(), n, length - 1, 2); // no 0

		double W = uniformlocal(rng2);
		// weighted average of 2 belief measures
		for (int i = 0; i < length - 1; i++)
			vs[i] = vs[i] * (1.0 - W) + W * v1[i];

		
		*/

		// start walk
		for (int steps = 0; steps < markov; steps++) {
			PerturbVectorMob1(vs, v1, length , n, noise); // with no 0


			res = CheckMonMob2additive2(v1.data(), n, length , aux1.data());


			// here any extra checks
			if (res && extrachecks != NULL) {
				// cast and call
				res = FF(&length, v1.data());
			}

			if (res) { //OK
				// save it
				copy(v1.begin(), v1.end(), vs.begin());
				success++;
			}
			else { // one step back
				fm_random_sort_flag = 0;
				// nothing, vs remains
			}
		}


		// no empty vv[0 + k * (length)] = 0;// emptyset


		for (int A = 0; A < length ; A++) vv[A + k * (length)] = vs[A ];
	}
	return success;

}


