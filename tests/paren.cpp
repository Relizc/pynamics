#include <bits/stdc++.h>

using namespace std;

int main() {
	long long N, A, B;
	cin >> N >> A >> B;
	
	string s;
	cin >> s;
	
	long long lo = LONG_LONG_MAX;
	long long state = 0;
	
	for (char c : s) {
		if (c == '(') {
			state ++;
		} else {
			state --;
		}
		
		lo = min(lo, state);
	}
	
	A = min(A, 2 * B); // what worths less
	
	long long ans = abs(state) / B * 2; // step 1: adjust sum to 0
	if (state < 0) {
		lo = min(0LL, lo + abs(state)); // step 2: floor the lo
	}
	
	long long k = ((abs(lo) + 1) / 2) * A;
	cout << ans + k << endl;
	
	
}
