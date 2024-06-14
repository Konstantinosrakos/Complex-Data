#include "main.h"

void merge(
    std::vector<std::pair<std::string,unsigned int>>& data,
    std::vector<std::pair<std::string,unsigned int>>& temp,
    int iLeft, int iRight, int iEnd, bool& c){

  int i = iLeft, j = iRight;
  while(i < iRight && j < iEnd){

    // Merge the 2 halves of in, into out
    if (data[i].first.compare(data[j].first) < 0)
      temp.push_back(data[i++]);
    else if (data[i].first.compare(data[j].first) > 0)
      temp.push_back(data[j++]);
    else if (data[i].first.compare(data[j].first) == 0){
      temp.push_back(std::make_pair(data[i].first, data[i].second + data[j].second));
      c = true; i++; j++;
    }
  }

  // When one pointer exceeds limit, only sorted values remain
  while (i < iRight)
    temp.push_back(data[i++]);
  while (j < iEnd)
    temp.push_back(data[j++]);
}

void mergeSort(std::vector<std::pair<std::string,unsigned int>>& data){

  int n = data.size(), width = 1;
  bool dupsExist = false;

  std::vector<std::pair<std::string,unsigned int>> temp;
  while (width < n){
    for (int i = 0; i < n; i += 2*width){
      merge(data, temp, i, std::min(i+width, n), std::min(i+2*width, n), dupsExist);
    }
    if (dupsExist){
      dupsExist = false;
      width = 1;
    } else
      width *= 2;
    
    n = temp.size();
    data.swap(temp);
    temp.clear();
  }
}

void performGroupbyAggregation(){

  std::ifstream rFile{"R.tsv"};
  std::ofstream groupbyFile{"Rgroupby.tsv"};

  std::string alnum;
  unsigned int value;

  std::vector<std::pair<std::string,unsigned int>> data;

  // Fill vector with .tsv data
  while(rFile >> alnum >> value)
    data.push_back(std::make_pair(alnum, value));

  mergeSort(data);

  // Export sorted array in .tsv format
  auto it = data.begin();
  for (; it != data.end(); ++it){
    groupbyFile << it->first << '\t' << it->second << std::endl;
  }

  std::cout << "Rgroupby.tsv created." << std::endl;
}
