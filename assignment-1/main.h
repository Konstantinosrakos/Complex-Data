#ifndef MAIN_H_
#define MAIN_H_

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <array>

// Buffer to save small amounts of data
struct Buffer{
  unsigned int maxSize;
  std::vector<std::pair<std::string,unsigned int>> data;
};

void performMergeJoin();
void performUnion();
void performIntersection();
void performDifference();
void performGroupbyAggregation();
void mergeSort(std::vector<std::pair<std::string,unsigned int>>& v);
void merge(
    std::vector<std::pair<std::string,unsigned int>>& in,
    std::vector<std::pair<std::string,unsigned int>>& out,
    int iLeft, int iRight, int iEnd);

#endif
