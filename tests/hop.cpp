// HOLY SHIT

#include <bits/stdc++.h>

using namespace std;

int main() {
	int N, D;
	cin >> N >> D;
	
	int numbers[N + 1];
	for (int i = 1; i <= N; i++) {
		int k;
		cin >> k;
		numbers[i] = k;
	}
	
	vector<int> dp(N + 1);
	dp[1] = numbers[1];
	
	deque<int> q;
	q.push_back(1);
	
	for (int i = 2; i <= N; i++) {

		dp[i] = dp[q.front()] + numbers[i];
		
		while (!q.empty() && (dp[q.back()] >= dp[i])) q.pop_back();
		q.push_back(i);
		if (q.front() <= i - D) q.pop_front();
	}
	
	cout << dp[N] << endl;
	
	return 0;
}

