import types

def foo():
    print "foo"

def fooWithArgs(a, b):
    print "a: " + str(a)
    print "b: " + str(b)

def fooWithInner():
    def inner():
        return "inner"
    return "outer"

'''
Returns a dictionary of the global functions,
    key: function name
    value: function object
'''
def getFunctions():
    globals_dict = globals()
    functionDict = dict()
    for key in globals_dict.keys():
        value = globals_dict[key]
        if isinstance(value, types.FunctionType):
            functionDict[key] = value

    return functionDict

def fooAfterGetFunctions():
    return "ahah"

if __name__ == '__main__':
    functionDict = getFunctions()
    print functionDict

def fooAfterMain():
    return "After! After! All I see or hear is after!"
