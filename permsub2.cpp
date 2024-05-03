#include <bits/stdc++.h>
#define ll unsigned long long

using namespace std;

ll func(int x){
	return (x%37 + 7919)*(x%37 + 7919);
}

ll hashes[200005];
ll phashes[200005];

ll hashed[200005];
ll phashed[200005];


int main() {
	
	for (int i = 0; i < 200001; i ++) {
		hashes[i] = func(i);
		
	}
	
	phashes[1] = hashes[1];
	for (int i = 2; i <= 200001; i ++) {
		phashes[i] = hashes[i] + phashes[i - 1];
	}
	
	int N, Q;
	
	cin >> N >> Q;
	
	for (int i = 1; i <= N; i ++) {
		int k;
		cin >> k;
		
		hashed[i] = hashes[k];
	}
	
	
	phashed[1] = hashed[1];
	
	for (int i = 2; i <= N; i ++) {
		phashed[i] = hashed[i] + phashed[i - 1];
	}
//	
//	for (int i = 0; i < N; i ++) {
//		cout << hashed[i] << endl;
//	}
//	
//	cout << " ====== " << endl;
//	
//	for (int i = 0; i < N; i ++) {
//		cout << phashed[i] << endl;
//	}
	
	for (int i = 0; i < Q; i ++) {
		int l, r;
		cin >> l >> r;
		
		int s = r - l  + 1;
		
		ll k = phashes[s];
		
		
		
		ll p = phashed[r] - phashed[l - 1];
		
		if (k == p) cout << 1 << endl;
		else cout << 0 << endl;
		
		//cout << k << " " << p << endl;
	}

}
