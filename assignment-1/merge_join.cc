#include "main.h"

void performMergeJoin(){

  std::ifstream rFile{"R_sorted.tsv"};
  std::ifstream sFile{"S_sorted.tsv"};
  std::ofstream joinFile{"RjoinS.tsv"};

  Buffer buf = {0};
  std::string rAlnum, sAlnum;
  unsigned int rValue, sValue;

  // Read the first line of each file
  sFile >> sAlnum >> sValue;
  rFile >> rAlnum >> rValue;

  while(rFile.peek() != std::ifstream::traits_type::eof()){

    // When the buffer is not empty, use the data or flush the buffer
    if (!(buf.data.empty())){
      rFile >> rAlnum >> rValue;

      // If R's alnum is equal to previous line's alnum,
      // export data using buffer to access S's already read data
      if (!(rAlnum.compare(buf.data.begin()->first)) &&
          rFile.peek() != std::ifstream::traits_type::eof()){

        for (auto it = buf.data.begin(); it != buf.data.end(); ++it)
          joinFile << rAlnum << '\t' << rValue << '\t' << it->second << '\n';
      }else{
        buf.data.clear();
      }

      if (buf.data.size() > buf.maxSize)
        buf.maxSize = buf.data.size();

      continue;
    }

    // Read next line depending on which pointer is ahead
    if (rAlnum.compare(sAlnum) < 0)
      rFile >> rAlnum >> rValue;
    else if (rAlnum.compare(sAlnum) > 0)
      sFile >> sAlnum >> sValue;

    // Export tuple and add data to the buffer
    while (!rAlnum.compare(sAlnum)){

      joinFile << rAlnum << '\t' << rValue << '\t' << sValue << '\n';
      buf.data.push_back(std::make_pair(sAlnum, sValue));
      sFile >> sAlnum >> sValue;
    }
  }
  std::cout << "RjoinS.tsv created. Max capacity: " << buf.maxSize << '\n';
}
