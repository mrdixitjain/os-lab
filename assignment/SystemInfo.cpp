
float userTime=0, kernelTime=0, idleTime=0, totalTime=0;
int interrupts=0;
float contextSwitches=0;
int freeMem=0, totalMem=0, swapSpace=0, freeSwap=0, swapPartitions=0;
int bootedTime=0;
float load=0;
int readTime, writeTime;
float processes=0;
float readRate=0, writeRate=0;

void calculateStat(){
	string line;
	ifstream fin;

// by default open mode = ios::in mode
	fin.open("/proc/stat");
	while(fin){
		getline(fin, line);
		int found = line.find("cpu");
		if(found!=string::npos)
			break;
	}
	vector<string> result1;
	boost::split(result1, line, boost::is_any_of(" "));
	userTime+=stoi(result1[3])+stoi(result1[2]);
	kernelTime+=stoi(result1[4]);
	idleTime+=stoi(result1[5]);
	totalTime+=userTime+kernelTime+idleTime;
// cout<<"time spent in user mode: "<<userTime*100/totalTime<<" %"<<endl;
// cout<<"time spent in kernel mode: "<<kernelTime*100/totalTime<<" %"<<endl;
// cout<<"time spent ideally: "<<idleTime*100/totalTime<<" %"<<endl;

	while(fin){
		getline(fin, line);
		int found = line.find("intr");
		if(found!=string::npos)
			break;
	}
	int found2=line.find(" ", 5);

	interrupts+=stoi(line.substr(5, found2-5));
// cout<<"interrupts: "<<interrupts<<endl;

	while(fin){
		getline(fin, line);
		int found = line.find("ctxt");
		if(found!=string::npos)
			break;
	}

	float n=std::stof(line.substr(5));
// cout<<"total context switches: "<<contextSwitches<<endl;

	while(fin){
		getline(fin, line);
		int found = line.find("btime");
		if(found!=string::npos)
			break;
	}
	bootedTime=std::stof(line.substr(6));
	contextSwitches+=n/bootedTime;
// cout<<"bootedTime: "<<bootedTime<<endl;

	while(fin){
		getline(fin, line);
		int found = line.find("processes");
		if(found!=string::npos)
			break;
	}
	processes=std::stof(line.substr(10));
	processes+=processes/bootedTime;


	fin.close();

	// fin.open("/proc/diskstats");
	// int reads, writes;
	// while(fin){
	// 	getline(fin, line);
	// 	vector<string> result5;
	// 	boost::split(result5, line, boost::is_any_of(" "));
	// 	cout<<"ok "<<result5[14]<<" "<<result5[18]<<endl;
	// 	reads+=stoi(result5[14]);
	// 	writes+=stoi(result5[18]);
	// 	//writeTime+=stoi(result5[19]);
	// }
	// readRate+=(float) reads/bootedTime;
	// writeRate+=(float) writes/bootedTime;

	fin.close();

	fin.open("/proc/meminfo");
	while(fin){
		getline(fin, line);
		int found=line.find("MemTotal");
		if(found!=string::npos){
			string size=line.substr(10);
			int found1=size.find(" ");
			totalMem+=stoi(size.substr(0, found1-1));
		}
		found=line.find("MemFree");
		if(found!=string::npos){
			string size=line.substr(9);
			int found1=size.find(" ");
			freeMem+=stoi(size.substr(0, found1-1));
		}
		found=line.find("SwapTotal");
		if(found!=string::npos){
			string size=line.substr(11);
			int found1=size.find(" ");
			swapSpace=stoi(size.substr(0, found1-1));
			swapPartitions+=1;
			
		}
		found=line.find("SwapFree");
		if(found!=string::npos){
			string size=line.substr(10);
			int found1=size.find(" ");
			freeSwap+=stoi(size.substr(0, found1-1));
		}
	}
// cout<<"total usable memory space: "<<totalMem<<" kbs"<<endl;
// cout<<"free memory space: "<<freeMem<<" kbs"<<endl;
// cout<<"total swap space: "<<swapSpace<<" kbs"<<endl;
// cout<<"used swap space: "<<swapSpace-freeSwap<<" kbs"<<endl;
// cout<<"total swap partitions: "<<swapPartitions<<endl;

	fin.close();

	fin.open("/proc/loadavg");
	getline(fin, line);
	vector<string> result;
	boost::split(result, line, boost::is_any_of(" "));
	load+=std::stof(result[2]);
    // cout<<"load on system for last 15 minutes: "<<result[2]<<endl;
	fin.close();
}
void outputStat() {
	int n=writeTime/readTime;
	cout<<"time spent in user mode: "<<userTime*100/totalTime/n<<" %"<<endl;
	cout<<"time spent in kernel mode: "<<kernelTime*100/totalTime/n<<" %"<<endl;
	cout<<"time spent ideally: "<<idleTime*100/totalTime/n<<" %"<<endl;
	cout<<"interrupts: "<<interrupts/n<<endl;
	cout<<"total context switches per second: "<<contextSwitches/n<<endl;
	cout<<"bootedTime: "<<bootedTime/n<<endl;
	cout<<"total usable memory space: "<<totalMem/n<<" kbs"<<endl;
	cout<<"free memory space: "<<freeMem/n<<" kbs"<<endl;
	cout<<"total swap space: "<<swapSpace/n<<" kbs"<<endl;
	cout<<"used swap space: "<<(swapSpace-freeSwap)/n<<" kbs"<<endl;
	cout<<"total swap partitions: "<<swapPartitions/n<<endl;
	cout<<"load on system for last 15 minutes: "<<load/n<<endl;
	cout<<"processes per second: "<<processes/n<<endl;
	cout<<"swap partition number "<<swapPartitions/n<<"and it's size is "<<swapSpace/n<<endl;
	// cout<<"read rate: "<<readRate/n<<endl;
	// cout<<"write rate: "<<writeRate/n<<endl;

	// readRate=0;
	// writeRate=0;
	userTime=0;
	kernelTime=0;
	idleTime=0;
	totalTime=0;
	interrupts=0;
	contextSwitches=0;
	freeMem=0;
	totalMem=0;
	swapSpace=0;
	freeSwap=0;
	swapPartitions=0;
	bootedTime=0;
	load=0;
	processes=0;
}


void reader() {
	std::chrono::seconds readInterval(readTime);
	while(true) {
		calculateStat();
		std::this_thread::sleep_for(readInterval);
	}
}

void clscr() {
	cout << "\033[2J\033[1;1H";
}

void writer() {
	std::chrono::seconds writeInterval(writeTime);
	while(true) {
		outputStat();
		std::this_thread::sleep_for(writeInterval);
		clscr();
	}
}

void startSystemInfo(int readRate, int writeRate) {
	readTime = readRate;
	writeTime = writeRate;

	std::thread readerThread(reader);
	std::thread writerThread(writer);

	readerThread.join();
	writerThread.join();
}

