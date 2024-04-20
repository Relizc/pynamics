#include <bits/stdc++.h>

using namespace std;

vector<int> smaller(const vector<int>& arr) {
	int n = arr.size();
	
	vector<int> result(n, 0);
	stack<int> st;
	
	for (int i = 0; i < n; i++) {
		
		while (!st.empty() && arr[st.top()] >= arr[i]) {
			st.pop();
		}
		
		result[i] = st.empty() ? 0 : (st.top() + 1);
		st.push(i);
	}
	
	return result;
}

int main() {
	int n;
	cin >> n;
	
	vector<int> arr(n);
	
	for (int i = 0; i < n; i++) {
		cin >> arr[i];
	}
	
	vector<int> s = smaller(arr);
	
	for (int i = 0; i < n; i++) {
		cout << s[i] << " ";
	}
	cout << "\n";
	
	return 0;
}

