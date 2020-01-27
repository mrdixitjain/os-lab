
void startProcessInfo(int id) {
fstream cmdlineFile;
fstream environFile;
fstream mapsFile;
fstream statFile;
fstream schedstatFile;

string line, temp;

cmdlineFile.open("/proc/" + to_string(id) + "/cmdline", ios::in);
environFile.open("/proc/" + to_string(id) + "/environ", ios::in);
mapsFile.open("/proc/" + to_string(id) + "/maps", ios::in);
statFile.open("/proc/" + to_string(id) + "/stat", ios::in);
schedstatFile.open("/proc/" + to_string(id) + "/schedstat", ios::in);

if (cmdlineFile.is_open()) {
getline(cmdlineFile, line);
cout << endl << "The command line with which the process was started: " << line << endl << endl;
cmdlineFile.close();
}

if (environFile.is_open()) {
getline(environFile, line);
cout << "The environment of the process: " << endl << line << endl;
environFile.close();
}

if (mapsFile.is_open()) {
cout << endl << "The contents of the address space of the process: " << endl << endl;
while(getline(mapsFile, line)) {
cout << line << endl;
}
cout << endl;
mapsFile.close();
}

if (statFile.is_open()) {

getline(statFile, line);

stringstream in(line);
for (int i = 0; i < 13; i++) {
in >> temp;
}

in >> temp;
cout << "The time spent by the process in the user mode: " << temp << endl;
in >> temp;
cout << "The time spent by the process in the kernel mode: " << temp << endl;

statFile.close();
}

if (statFile.is_open()) {

getline(statFile, line);

stringstream in(line);

in >> temp;
cout << "The time spent by the process in running: " << temp << endl;
in >> temp;
cout << "The time spent by the process in waiting: " << temp << endl;

statFile.close();
}
}
