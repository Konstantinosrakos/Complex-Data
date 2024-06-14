#include "main.h"

void performUnion(){

  std::ifstream rFile{"R_sorted.tsv"};
  std::ifstream sFile{"S_sorted.tsv"};
  std::ofstream unionFile{"RunionS.tsv"};

  std::string rAlnum, sAlnum;
  unsigned int rValue, sValue;
  std::pair<std::string,unsigned int> prevTuple;

  // Read the first line of each file
  sFile >> sAlnum >> sValue;
  rFile >> rAlnum >> rValue;

  while (rFile.peek() != std::ifstream::traits_type::eof()){

    // Avoid duplicates in the same file
    if (rAlnum.compare(prevTuple.first) == 0
        && rValue == prevTuple.second){
      rFile >> rAlnum >> rValue;
      continue;
    } else if ((sAlnum.compare(prevTuple.first) == 0
        && sValue == prevTuple.second)){
      sFile >> sAlnum >> sValue;
      continue;
    }

    // Export tuple from the smallest of S or R
    // when S and R are equal, avoid duplicates
    if (rAlnum.compare(sAlnum) < 0){
      unionFile << rAlnum << '\t' << rValue << '\n';
      prevTuple = std::make_pair(rAlnum, rValue);
      rFile >> rAlnum >> rValue;
    } else if (rAlnum.compare(sAlnum) > 0){
      unionFile << sAlnum << '\t' << sValue << '\n';
      prevTuple = std::make_pair(sAlnum, sValue);
      sFile >> sAlnum >> sValue;
    } else if (rValue < sValue){
      unionFile << rAlnum << '\t' << rValue << '\n';
      prevTuple = std::make_pair(rAlnum, rValue);
      rFile >> rAlnum >> rValue;
    } else if (rValue > sValue){
      unionFile << sAlnum << '\t' << sValue << '\n';
      prevTuple = std::make_pair(sAlnum, sValue);
      sFile >> sAlnum >> sValue;
    } else{
      unionFile << rAlnum << '\t' << rValue << '\n';
      prevTuple = std::make_pair(rAlnum, rValue);
      sFile >> sAlnum >> sValue;
      rFile >> rAlnum >> rValue;
    }
  }

  while (sFile.peek() != std::ifstream::traits_type::eof()){
    unionFile << sAlnum << '\t' << sValue << '\n';
    sFile >> sAlnum >> sValue;
  }
  std::cout << "RunionS.tsv created." << '\n';
}

void performIntersection(){

  std::ifstream rFile{"R_sorted.tsv"};
  std::ifstream sFile{"S_sorted.tsv"};
  std::ofstream intersectionFile{"RintersectionS.tsv"};

  std::string rAlnum, sAlnum;
  unsigned int rValue, sValue;
  std::pair<std::string,unsigned int> prevTuple;

  // Read the first line of each file
  sFile >> sAlnum >> sValue;
  rFile >> rAlnum >> rValue;

  while (rFile.peek() != std::ifstream::traits_type::eof()){

    // Avoid duplicates in the same file
    if (rAlnum.compare(prevTuple.first) == 0
        && rValue == prevTuple.second){
      rFile >> rAlnum >> rValue;
      continue;
    } else if ((sAlnum.compare(prevTuple.first) == 0
        && sValue == prevTuple.second)){
      sFile >> sAlnum >> sValue;
      continue;
    }

    // Export tuple when R's tuple is equal to S's tuple
    if (!(rAlnum.compare(sAlnum)) && rValue == sValue){
      intersectionFile << rAlnum << '\t' << rValue << '\n';
      prevTuple = std::make_pair(rAlnum, rValue);
      sFile >> sAlnum >> sValue;
      rFile >> rAlnum >> rValue;
    } else if (rAlnum.compare(sAlnum) < 0){
      rFile >> rAlnum >> rValue;
    } else if (rAlnum.compare(sAlnum) > 0){
      sFile >> sAlnum >> sValue;
    } else if (rValue < sValue){
      rFile >> rAlnum >> rValue;
    } else if (rValue > sValue){
      sFile >> sAlnum >> sValue;
    }
  }

  std::cout << "RintersectionS.tsv created." << '\n';
}

void performDifference(){

  std::ifstream rFile{"R_sorted.tsv"};
  std::ifstream sFile{"S_sorted.tsv"};
  std::ofstream differenceFile{"RdifferenceS.tsv"};

  std::string rAlnum, sAlnum;
  unsigned int rValue, sValue;
  std::pair<std::string,unsigned int> prevTuple;

  // Read the first line of each file
  sFile >> sAlnum >> sValue;
  rFile >> rAlnum >> rValue;

  while (rFile.peek() != std::ifstream::traits_type::eof()){

    // Avoid duplicates in the same file
    if (rAlnum.compare(prevTuple.first) == 0
        && rValue == prevTuple.second){
      rFile >> rAlnum >> rValue;
      continue;
    } else if ((sAlnum.compare(prevTuple.first) == 0
        && sValue == prevTuple.second)){
      sFile >> sAlnum >> sValue;
      continue;
    }

    // Export tuple when R's tuple is smaller than S's, since files
    // are sorted this means a tuple exists in R and not in S
    if (!(rAlnum.compare(sAlnum)) && rValue == sValue){
      sFile >> sAlnum >> sValue;
      rFile >> rAlnum >> rValue;
    } else if (rAlnum.compare(sAlnum) < 0){
      differenceFile << rAlnum << '\t' << rValue << '\n';
      prevTuple = std::make_pair(rAlnum, rValue);
      rFile >> rAlnum >> rValue;
    } else if (rAlnum.compare(sAlnum) > 0){
      sFile >> sAlnum >> sValue;
    } else if (rValue < sValue){
      differenceFile << rAlnum << '\t' << rValue << '\n';
      prevTuple = std::make_pair(rAlnum, rValue);
      rFile >> rAlnum >> rValue;
    } else if (rValue > sValue){
      sFile >> sAlnum >> sValue;
    }
  }
  std::cout << "RdifferenceS.tsv created." << '\n';
}
