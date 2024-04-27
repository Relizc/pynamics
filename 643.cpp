#include <bits/stdc++.h>

using namespace std;

int stones[50002];

int main() {
	
	int n, k;
	cin >> n >> k;
	
	for (int i = 0; i < n; i ++) {
		cin >> stones[i];
	}
	
	sort(stones, stones + n);
	
	int cur = -1;
	int cur_index = 0;
	int cnt = 0;
	
	int counts[n];
	
	for (int i = 0; i < n; i ++) counts[i] = 0;
	
	for (int i = 0; i < n; i ++) {
		if (cur == -1) cur = stones[i];
		else {
			if (stones[i] - cur > k) {
				counts[cnt] = i - cur_index + 1;
				
				cur = -1;
				cur_index = i;
				cnt ++;
			}
		}
	}
	
	for (int i = 0; i < n; i ++) {
		cout << counts[i] << endl;
	}
	
}
