import  os,sys
from math import sqrt,ceil

def compute(x,y):
 return(x+ y)* (x-y)
def printResults():
   res=compute( 5,3 )
 print("Result is test:",res)


class Test:
  def __init__( self):
        self.data=[1,2, 3,4]
 def get_data(self):
     return self.data

def broken_function(x,y):
	if x>y:
        print( "x is greater")
    else:
        print("y is greater")    

def main():  printResults();t=Test();print(t.get_data());broken_function(2,10)
if __name__=="__main__":
 main()
