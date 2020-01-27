#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <iterator>
#include <thread>
#include <bits/stdc++.h>
#include <boost/algorithm/string.hpp>

using namespace std;

#include "machineInfo.cpp"
#include "SystemInfo.cpp"
#include "ProcessInfo.cpp"
int main( int argc, char** argv){
	if(argc < 2) {
		cout<< "Too few arguements"<<endl;
		return 0;
	}
	else if( argc == 1){
		machineInfo();
	}
	else if( argc == 2){
		// cout<<argv[1]<<endl;
		startProcessInfo(atoi(argv[1]));
	}
	else if(argc == 3){
		startSystemInfo(atoi(argv[1]), atoi(argv[2]));
	}
	return 0;
}