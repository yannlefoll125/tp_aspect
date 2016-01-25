
def wrap(f, *args, **kwargs):
    print "wrap"
    for a in args:
        print a

    for (k, v) in kwargs.iteritems():
        print k + "=>" + str(v)

    foo(*args, **kwargs)

def foo(a, b, c):
    print "foo"
    print "a: " + str(a)
    print "b: " + str(b)
    print "c: " + str(c)



if __name__ == '__main__':
    #The following calls pass the same values to foo
    wrap(foo, 1, c=2, b=3)
    wrap(foo, 1, 2, 3)
    wrap(foo, a=1, b=2, c=3)
    wrap(foo, b=2, a=1, c=3)


    #The following calls is illegal, because the positional arguments
    #must all be placed before the named arguments.
    #wrap(foo, a=1, 2, c=3)


