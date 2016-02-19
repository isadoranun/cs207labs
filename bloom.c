//I am working with Avery Faller and Reinier Maat
#include "bloom.h"

index_t hash1(bloom_filter_t *B, key_t k){

	return k % B->size;

}

index_t hash2(bloom_filter_t *B, key_t k){

	//Copied from https://gist.github.com/badboy/6267743
	index_t m;

	m = B->size;

	k = (~k) + (k << 21); 
	k = k ^ (k >> 24);
	k = (k + (k << 3)) + (k << 8); 
	k = k ^ (k >> 14);
	k = (k + (k << 2)) + (k << 4);
	k = k ^ (k >> 28);
	k = k + (k << 31);
	return k % m;
}

index_t get(bloom_filter_t *B, key_t k, index_t idx){

	index_t storage_integer = table[idx >> 6]
	index_t left_over = 


int main(){

	index_t *t;
	bloom_filter_t filter = {100,0,t};
	printf("%d ", hash1(&filter, 0));	
	printf("%d ", hash1(&filter, 1));	
	printf("%d ", hash1(&filter, 2));
	printf("%d ", hash1(&filter, 3));	
	printf("%d ", hash1(&filter, 13));	
	printf("%d ", hash1(&filter, 97));	

	return 0;
}

