import types
import copy

def copyFunction(f, f_name):
    return types.FunctionType(f.func_code, f.func_globals, name = f_name,
                            argdefs = f.func_defaults,
                            closure = f.func_closure)



def foo(a, b, c):
    print "foo"
    print "a: " + str(a)
    print "b: " + str(b)
    print "c: " + str(c)


if __name__ == '__main__':


    g = copyFunction(foo, "g")
    foo(1, 2, 3)
    g(4, 5, 6)

    print "g.name: " + g.func_name


    h = copy.deepcopy(foo)
    h(7, 8, 9)

    #Tests

    print "foo: " + str(foo)
    print "g: " + str(g)
    print "h: " + str(h)

    assert g is not foo
    assert h is not foo
