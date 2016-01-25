import types

globals_dict = globals()
dir_dict = dir()

def foo():
    print "foo"

def fooWithArgs(a, b):
    print "a: " + str(a)
    print "b: " + str(b)

def getFunctions():
    functionDict = dict()
    for key in globals_dict.keys():
        value = globals_dict[key]
        if isinstance(value, types.FunctionType):
            functionDict[key] = value

    return functionDict

if __name__ == '__main__':
    functionDict = getFunctions()
    print functionDict


