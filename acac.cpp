#include <bits/stdc++.h>

using namespace std;

int main() {
	int N;
	cin >> N;
	
	if (N == 1) {
		cout << 0 << endl;
		return 0;
	}
	
	int values[N];
	
	for (int i = N - 1; i >= 0; i --) {
		cin >> values[i];
	}
	
	//for (int i = 0; i < N; i ++) cout << values[i] << endl;
	
	stack<int> s;
	
	int nearest[N];
	for (int i = 0; i < N; i ++) nearest[i] = INT_MAX;
	nearest[0] = 0;
	
	for (int i = 0; i < N; i ++) {
		while (!s.empty() && (values[s.top()] > values[i])) {
			s.pop();
			
			int dist = i;
			if (!s.empty()) dist = i - s.top() - 1;
			
			cout << i << " " << dist << endl;
			
			nearest[N - dist - 1] = min(N - i, nearest[ N - dist - 1]);
		}
		
		s.push(i);
	}
	
	for (int i = 0; i < N; i ++) {
		cout << nearest[i] << " ";
	}
	cout << endl;
	
	while (!s.empty()) {
		
		cout << s.top() << " ";
		
		s.pop();
		
		int dist = N;
		
		
		
		if (!s.empty()) dist = dist - s.top() - 1;
		
		cout << dist << endl;
	}
}
