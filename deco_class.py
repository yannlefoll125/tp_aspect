import traceback, sys

class deco(object):
    def __init__(self, name):

        #Name of the function we want in the call stack to print the stack trace
        self.name = name

    '''
    __call__ will be executed anytime the object 'deco' is called.
    fn will hold the reference to the function decorated. Each time this function will be executed in the code, __call__ will be executed
    '''
    def __call__(self, fn):

        '''
        Defines the behaviour of the decorator. When the function referenced by fn is executed, wrapper will be executed with the given parameters
        '''
        def wrapper(*args):

            #extract_stack() returns the call stack as a list of 4-tuples, in which the function name is given at index 2)
            stack_list = traceback.extract_stack()

            #We first check the call stack for a function named 'self.name'. If found, print the stack trace
            if self.isInStack(stack_list, self.name):
                traceback.print_stack()

            #The function is called anyway
            fn(*args)
        return wrapper

    '''
    isInStack goes through the stack_list given in argument, and checks if the function name given in argument is in it
    '''
    def isInStack(self, stack_list, fun_name):
        ret = False
        for s in stack_list:
            if s[2] == fun_name:
                ret = True
                break
        return ret



'''
Functions used to call the decorated function 'test' through different call stacks.
'''
def foo3():
    return test()

def foo2():
    return foo3()

def foo1(bar):
    return foo2()

def bar():
    return test()

#This line decorates the function test, with "bar" as argument. It creates an instance of deco with attribute self.name = bar
#Each time test is called, the function __call__ of this instance will be executed.
@deco("bar")
def test():
    return "test function"

if __name__ == '__main__':
    print "Calling foo1(). Should not print the stack"
    foo1(45)

    print "Calling bar(). Should print the stack"
    bar()

