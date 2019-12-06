#include<stdio.h>
#include<stdlib.h>
#include<limits>
#include<vector>
#include<algorithm>
#include<iostream>

using namespace std;

// Compares according to the field "real" of the struct.
int sortcol(const void *a, const void *b){
    float *x = (float*)a;
    float *y = (float*)b;
    int my_dimension = 6;
    printf("oops: %f \n", x[my_dimension-1]);
    return x[my_dimension-1] < y[my_dimension-1] ;
}

bool sortcol2( const vector<float>& v1,
             const vector<float>& v2 ) {
    printf("%d \n", v1.size());
    return v1[v1.size()] < v2[v2.size()];
}

int compare ( const void *pa, const void *pb ) {
    const int *a = *(const int **)pa;
    const int *b = *(const int **)pb;
    return (a[5] < b[5]) - (a[5] > b[5]);
}

int main()
{
    const char  *fname = "./temp_result_100D_top25_1000000/hash_proj_random_opt_1";
    FILE *fp = fopen(fname, "w");
    if (!fp)
    {
        printf("Could not create %s\n", fname);
        return -1;
    }
    else{
        printf("yeah it works");
    }
    
    // cout<<DBL_EPSILON<<endl;
//    double temp =  std::numeric_limits<double>::epsilon();
//    cout << temp <<endl;
   
    
    return 0;

    
}