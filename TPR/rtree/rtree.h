/* rtree.h
   this file defines the class RTree*/

#ifndef __RTREE
#define __RTREE
//------------------------------------------------------------
#include "../func/gendef.h"
#include "../heap/heap.h"
#include "../blockfile/max_list.h"
#include "myentry.h"
//------------------------------------------------------------
class LinList;
class SortedLinList;
class Cache;
class RTNode;
class Entry;
class MyEntry;
class MaxK_List;


//------------------------------------------------------------
struct TPRSortMbr
{
	int index;
	int dimension;
	int st,ed;
	float *bounces;
	float *velocity;
	float *centermbr;
	float *centervmbr;
	float cntrd_dist;
};
//------------------------------------------------------------
class RTree : public Cacheable
{
public:
//--===on disk===--
	int dimension;                       
	int num_of_data;	                 
    int num_of_dnodes;	                 
    int num_of_inodes;	                 
	int root;                            
	bool root_is_data;                   
//--===others===--
	RTNode *root_ptr;
    bool *re_level;  
    LinList *re_data_cands; 
	LinList *deletelist;
//--===functions===--
    RTree(char *fname, Cache* c);
    RTree(char *_dsfname, char *_tfname, int _blen, Cache *_c, int _dimension,
			float *_qmbrlen, float *_qvbr, float _qst, float _qed);

    ~RTree();
	void del_root();
	bool FindLeaf(Entry *e);
    int get_num() { return num_of_data; }
	void insert(Entry *d);
	void load_root();  
	float *moving_sect(Entry *_e1, Entry *_e2, float _st, float _ed);
	//void rangeQuery(Entry *_q, float _st, float _ed, SortedLinList *res);
	void rangeQuery(Entry *_q, float _st, float _ed, int& _rsltcnt);
	void read_header(char *buffer);      
	void write_header(char *buffer);
	//--===added for tpr*===--
	int path[4]; //the path decided for choosing an entry
	int root_lvl; //level of the root
	Heap *pathhp;  //the heap used in choosing the optimal path for inserting an entry
	float *qmbrlen; //the lengths of the target mbr
	float *qvbr; // the target vbr
	float qst, qed; //the target query interval
	float time; //this is the current time of the tree
	int maxChoosePathNA; //maximum node accesses in ChoosePath
	bool emergency;

	void check_path(Entry *_newe, float _minpen);
	float choose_path(Entry *_newe);
	void delete_entry(Entry *_olde);

	// Added by Sicong
	float get_maxscore(float* p_mbr, float* query);

	// Added by Sicong
	int BRS(int top_k, MaxK_List* list, float* query);

};


#endif // __RTREE
