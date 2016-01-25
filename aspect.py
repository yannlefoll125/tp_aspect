
import inspect
import re


pre_advice_pattern = re.compile("_c.*")
post_advice_pattern = re.compile("exc.*")
around_advice_pattern = re.compile("get.*")

def before_call(joint_point, advice):
    def inner(*args, **kwargs):
        advice()
        return joint_point(*args, **kwargs)
    return inner

def after_call(joint_point, advice):
    def inner(*args, **kwargs):
        ret = joint_point(*args, **kwargs)
        advice()
        return ret
    return inner

def around_call(joint_point, before_advice, after_advice):
    pre = before_call(joint_point, before_advice)
    return after_call(pre, after_advice)


def pre_advice():
    print "pre_advice function"

def post_advice():
    print "post_advice function"

def foo(a, b, c):
    print "foo"
    print "a: " + str(a)
    print "b: " + str(b)
    print "c: " + str(c)

def my_import(name):


    print "import is call with name: " + name
    module =  __import__(name)
    fun_list = inspect.getmembers(module, inspect.isfunction)
    fun_list += inspect.getmembers(module, inspect.isbuiltin)



    for (name, fun) in fun_list:
        if around_advice_pattern.match(name) != None:
            setattr(module, name, around_call(fun, pre_advice, post_advice))
        elif pre_advice_pattern.match(name) != None:
            setattr(module, name, before_call(fun, pre_advice))
        elif post_advice_pattern.match(name) != None:
            setattr(module, name, after_call(fun, post_advice))
    return module

sys = my_import('sys')

if __name__ == '__main__':
    pre_foo = before_call(foo, pre_advice)

    print "Pre advised foo: \n"
    pre_foo(1, 2, c=3)

    post_foo = after_call(foo, post_advice)

    print "\nPost advised foo: \n"
    post_foo(4, 5, 6)

    around_foo = around_call(foo, pre_advice, post_advice)

    print "\nPre and Post advised foo: \n"
    around_foo(7, 8, 9)

    #Tests
    print str(pre_foo)
    print str(post_foo)
    print str(around_foo)


    print "Aspect tests, on module sys"

    print "\ntest on sys._clear_type_cache() function (pre_advice)\n"
    sys._clear_type_cache()


    print "\ntest on sys.exc_clear() function (post_advice)\n"
    sys.exc_clear()


    print "\ntest on sys.getrecursionlimit() function (around_advice)\n"
    sys.getrecursionlimit()


    print "\ntest on sys._getframe() function (no advice)\n"
    sys._getframe()
