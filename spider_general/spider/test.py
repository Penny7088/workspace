#coding=utf-8 

def originalFunc(): 
    print 'this is original function!' 
     
def modifiedFunc(): 
    modifiedFunc=1 
    print 'this is modified function!' 
     
def main(): 
    originalFunc() 
     
if __name__=='__main__': 
    originalFunc=modifiedFunc 
    main()