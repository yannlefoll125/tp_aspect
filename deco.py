import traceback

def traceback_deco(fn):
    def wrapper(arg):
        ret = fn(arg)
        traceback.print_stack()
        return ret
    return wrapper

def foo3(bar):
    return test(bar)

def foo2(bar):
    return foo3(bar)

def foo1(bar):
    return foo2(bar)

@traceback_deco
def test(a):
    return "test function, arg value: " + str(a)

if __name__ == '__main__':
    print "Calling foo1(45)"
    foo1(45)

    print "Calling foo2(46)"
    foo2(46)

