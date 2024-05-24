
#include <bits/stdc++.h>

using namespace std;

int minScoreJumpscotch(int N, int D, const vector<int>& values) {
	
}

int main() {
	int N, D;
	
	cin >> N >> D;
	
	
	vector<int> values;
	
	for (int i = 0; i < N; i ++) {
		int k;
		cin >> k;
		
		values.push_back(k);
	}
	
	vector<int> dp(N, INT_MAX);

	dp[0] = values[0];
	
	for (int i = 1; i < N; i++) {
		
		for (int j = max(0, i - D); j < i; j++) {
			
			dp[i] = min(dp[i], dp[j] + values[i]);
			
		}
		
	}
	
	cout << dp[N - 1] << endl;
}

