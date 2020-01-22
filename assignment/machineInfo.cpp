


int machineInfo() 
{  

	string line; 
	ifstream fin; 

	// by default open mode = ios::in mode 
	fin.open("/proc/cpuinfo");
	int processors;
	int cpu_cores;
	string processor_type="";
	string clock_speed="";
	while (fin) { 
		// Read a Line from File 
		getline(fin, line); 

		int found = line.find("processor");
		if(found!=string::npos)
			processors++;
		if(cpu_cores==0){
			found=line.find("cpu cores");
			if(found!=string::npos){
				cpu_cores=(int)(line[12]-'0');
			}
		}
		if(clock_speed==""){
			found=line.find("model name");
			if(found!=string::npos){
				clock_speed=line.substr(46);
			}
		}
		if(processor_type==""){
			found=line.find("model name");
			if(found!=string::npos){
				processor_type=line.substr(13);
			}
		}



		// Print line in Console 
	} 
	cout<<"processor type: "<<processor_type<<endl;
	cout<<"number of processors: "<<processors<<endl;
	cout<<"number of cpu cores: "<<cpu_cores<<endl;
	cout<<"clock speed: "<<clock_speed<<endl;
	fin.close();

	fin.open("/proc/version");
	string version;
	getline(fin, line);
	int found = line.find("version");
	int end = line.find("(");
	version=line.substr(found+8, end-found-9);
	cout<<"linux kernel version: "<<version<<endl;
	fin.close();

	cout<<"\nMemory info of device: "<<endl;
	fin.open("/proc/meminfo");
	while(fin){
		getline(fin, line);

		cout<<line<<endl;
	}

	fin.close();

	fin.open("/proc/uptime");
	getline(fin, line);
	fin.close();
	found=line.find(" ");
	string time = line.substr(0, found);
	float tsec= std::stof(time);
	int days, hour, minute, sec;
	days=(int)(tsec/86400);
	tsec=tsec-days*86400;
	hour=(int)(tsec/3600);
	tsec-=hour*3600;
	minute=(int)(tsec/60);
	tsec-=minute*60;
	sec=tsec;
	cout<<"time from last reboot(day:hour:minute:sec): "<<days<<":"<<hour<<":"<<minute<<":"<<sec<<endl;

	
	return 0; 
} 
