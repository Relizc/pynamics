#include <bits/stdc++.h>

using namespace std;


mt19937_64 rng1(chrono::steady_clock::now().time_since_epoch().count());
std::uniform_int_distribution<std::mt19937::result_type> rng(0, 32767);

unsigned long long hashes[20001];
unsigned long long prefix_hashes[20001];

int nums[20001];
unsigned long long hashed_nums[20001];

unsigned long long prefix_nums[20001];



int main() {
	for (int i = 1; i <= 20001; i ++ ) {
		unsigned long long k = rng1();
		hashes[i] = k;
	}
	
	prefix_hashes[1] = hashes[1];
	for (int i = 2; i <= 20001; i ++) {
		prefix_hashes[i] = prefix_hashes[i - 1] + hashes[i]; 
	}
	
//	for (int i = 0; i < 128; i ++) {
//		cout << hashes[i] << " " << prefix_hashes[i] << endl;
//	}
	
	int N, Q;
	cin >> N >> Q;
	
	for (int i = 0; i < N; i ++) {
		cin >> nums[i];
		hashed_nums[i] = hashes[nums[i]];
	}
	
	//cout << " ======== " << endl;
	
	prefix_nums[1] = hashed_nums[0];
	for (int i = 2; i <= N; i ++) {
		prefix_nums[i] = prefix_nums[i - 1] + hashed_nums[i - 1];
		
		//cout << prefix_nums[i] << endl;
	}

	
//	for (int i = 0; i < N; i ++) {
//		cout << hashed_nums[i] << " " << prefix_hashes[i] << endl;
//	}
	
	for (int i = 0; i < Q; i ++) {
		int l, r;
		cin >> l >> r ;
		
		int s = r - l + 1;
		
		//cout << s << " " << prefix_hashes[s] << endl;
		
		unsigned long long hash_sum = prefix_hashes[s - 1];
		
		unsigned long long array_sum = prefix_nums[r - 1] - prefix_nums[l - 1];
		
		cout << (hash_sum == array_sum) << endl;
	}
	
	
	
	
}
