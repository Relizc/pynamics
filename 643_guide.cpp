#include <bits/stdc++.h>

using namespace std;

int stones[50002];

int main() {
	
	freopen("diamond.in", "r", stdin);
	freopen("diamond.out", "w", stdout);
	
	int n, k;
	cin >> n >> k;
	
	for (int i = 0; i < n; i ++) {
		cin >> stones[i];
	}
	
	sort(stones, stones + n);
	
	// partial hint from usaco guide
	
	int take[n]; // take[x]: the maximum stones that can put in the case starting from x
	
	
//	for (int i = 0; i < n; i ++) take[n] = -1;
//	
//	for (int i = 0; i < n; i ++) {
//		
//		
//		
//		for (int j = i; j < n; j ++) {
//			
//			cout << i << " " << j << endl;
//			
//			if (stones[j] - stones[i] > k) {
//				take[i] = j - i + 1; // distance
//				break;
//			}
//		}
//	}
	
	int l = 0, r = 0;
	
	while (l < n) {
		
		while (r < n) {
			
			bool ok = (stones[r] - stones[l] <= k);
			if (!ok) break;
			
			r ++;
		}
		
		take[l] = r - l;
			
		l ++;
	}
	
    //sort(take, take + n);
	
	int nextbest[n + 2]; // negative direction
	nextbest[n] = 0;
	
	for (int i = n - 1; i >= 0; i --) {
		nextbest[i] = max(nextbest[i + 1], take[i]);
	}
	
	// compute first two maximum
	int m = 0;
	for (int i = 0; i < n; i ++) {
		m = max(m, take[i] + nextbest[i + take[i]]);
	}
	cout << m << endl;
	
}
