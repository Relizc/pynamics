
#include <bits/stdc++.h>

using namespace std;

int main() {
	int N, A, B;
	cin >> N >> A >> B;
	
	string s;
	cin >> s;
	
	int l = 0; // ((
	int r = 0; // ))
	int x = 0; // )(   )()(
	
	int cost = 0;
	
	for (int i = 0; i < 2 * N; i += 2) {
		if (s[i] == '(' && s[i + 1] == '(') {
			l ++;
		} else if (s[i] == ')' && s[i + 1] == ')') {
			r ++;
		} else if (s[i] == ')' && s[i + 1] == '(') {
			x ++;
		}
	}
	
	if (l > r) {
		l -= r;
		cost += min(A * r, B * 2 * r);
		r = 0;
	} else if (r > l) {
		r -= l;
		cost += min(A * l, B * 2 * l);
		l = 0;
	} else {
		cost += min(A * r, B * 2 * r);
		l = 0;
		r = 0;
	}
	
	// at this point at least l or r should be 0, or both
	
	int rem = max(l, r);
	if (rem == 0) {
		cout << cost << endl;
		return 0;
	}
	
	cost += min(A * x, 2 * B * x) + rem * B;
	
	cout << cost << endl;
}
