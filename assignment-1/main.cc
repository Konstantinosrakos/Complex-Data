#include "main.h"

int main(){
  short keyboardInput;

  do{
    std::cout << "No.\tAction\n1\tMerge-join\n"
        "2\tUnion\n3\tIntersection\n4\tSet-difference\n"
        "5\tGroupby-aggregation\n6\tExit\n"
        "Action (No.): ";
    std::cin >> keyboardInput;
  }while (keyboardInput < 1 || keyboardInput > 6);

  switch (keyboardInput){
    case(1):
      performMergeJoin();
      break;
    case(2):
      performUnion();
      break;
    case(3):
      performIntersection();
      break;
    case(4):
      performDifference();
      break;
    case(5):
      performGroupbyAggregation();
      break;
    default:
      break;
  }
}
