#include <iostream>
#include <fstream>
using namespace std;

int main()
{
    char data[100];
    //open a file in write mode
    ofstream wfile;
    wfile.open("trang.txt");
    cout<<"Write to file"<<endl;
    cin.getline(data,100);
    wfile<<data<<endl;
    cin >> data;
    //cin.ignore();
    wfile<<data<<endl;
    wfile.close();

    ifstream rfile;
    rfile.open("trang.txt");
    cout<<"Read from file"<<endl<<"==========="<<endl;
    rfile.getline(data,100);
    cout<<data<<endl;
    rfile>>data;
    cout<<data<<endl;
    rfile.close();
    return 0;
}
