# Partie 1

## 1.1 PATH

Initialement, `wc` appelle `/usr/bin/wc` (comme indiqué par le résultat de `which wc`)

Mon script bash *wc* affiche "hi", puis appelle *wc* en lui passant l'ensemble des arguments.

Pour appeler mon script lorsque j'appelle wc dans un terminal, je l'ajoute au path

```bash
export PATH="$(pwd):"$PATH
```

* Remarque : au départ, j'ai ajouté mon *wc* à la fin du PATH, et donc le *wc* d'orignine était d'abord appelé. L'ordre des emplacements a donc une importance dans la variable PATH 

`which wc` affiche maintenant `<mon_directory>/wc`

* Remarque : dans une première version du script, j'appelais *wc* sans donner le chemin complet du *wc* d'origine. Mon script s'appelais donc récursivement. Il faut appeler le *wc* d'originie avec `/usr/bin/wc/`

## 1.2 LD_PRELOAD

Mon executable `hello` appelle simplement `printf("Hellow World!\n")`

`hello` est compilé avec `gcc -o hello hello.c`

Pour savoir quelle fonction de la librairie standard est appelée pour mon `printf`, j'exécute `nm hello` qui conne comme résultat:

```
[...]
T main
U puts@@GLIBC_2.2.5
[...]
```

C'est donc `int puts(const char *s)` qui est appelée pour mon `printf`

L'idée est de définir une implémentation "personnelle" de `puts`, et indiquer à l'exécution de `hello` d'utiliser cette implémentation de `puts`, et non celle de la libc.

Cette fonction est implémentée dans `hack.c`, et est compilée en librairie dynamique avec la commande `gcc -share -fPIC -o hack.so hack.c`.

Pour indiquer à `hello` qu'il doit aller chercher `puts` en priorité dans la librairie `hack.so`, on modifie la variable d'environnement LD_PRELOAD lors de l'exécution : 

```bash
LD_PRELOAD=./hack.so ./hello
```

* Remarque : Dans un premier temps, j'ai implémenté mon `puts` en utilisant `printf`. Mais comme `printf` est remplacée par `puts`, j'appelais récursivement ma propre implémentation de `puts` (même erreur que pour le 1.1). J'ai donc implémenté mon `puts` avec l'appel système `write`

## 1.3 Décorateurs Python

### 1.3.1 Décorateur pour afficher la trace d'appel

Ressources utilisées : 

1. http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/ pour mieux comprendre la notion de décorateur python
2. https://docs.python.org/2/library/traceback.html et http://stackoverflow.com/questions/3702675/how-to-print-the-full-traceback-without-halting-the-program pour l'utilisation du module `traceback`

L'objectif est d'écrire un décorateur permettant d'afficher la pile d'appel de la fonction décorée, c'est à dire la suite d'appels successifs menant à l'appel de la fonction décorée.   

Voici le code du décorateur (deco.py) :  

```python
import traceback, sys

def traceback_deco(fn):
    def wrapper(arg):
        ret = fn(arg)
        traceback.print_stack(file=sys.stdout) #Print on stdout, instead of stderr
        return ret
    return wrapper
```

`traceback_deco(fn)` prend en argument la référence d'une fonction, et retourne la référence de fonction interne `wrapper(arg)`. 

Ainsi, si on exécute la ligne suivante :

```python
decorated = traceback_deco(a_function)
```

`decorated` fera référence à la fonction `wrapper`, dont la variable locale `fn` fera référence à la fonction `a_function`. (En effet, en python, une fonction interne mémorise l'état de la fonction englobante au moment de la définition de cette fonction interne [cf. ref 1, ch. 8]) 

Un appel à la fonction `decorated` appellera donc la fonction `wrapper` où `fn == a_function`, avec l'argument passé à `decorated`.

La ligne :

```python
decorated(2)
```

exécutera donc `a_function` avec `2` comme argument, et affichera la trace de la pile d'appel jusqu'à la fonction décorée `decorated`.

Dans le fichier `deco.py`, j'ai illustrée le fonctionnement avec les instructions suivantes :

```python
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
```

Syntaxe : le bout de code 

```python
@traceback_deco
def test(a):
    return "test function, arg value: " + str(a)
```

est équivalent à

```python
def test(a):
    return "test function, arg value: " + str(a)

test = traceback_deco(test)
```

c'est à dire une redéfinition de `test` décorée par `traceback_deco`, en gardant le même identifiant.

L'exécution de `deco.py` donne la sortie suivante :

```
Calling foo1(45)
  File "deco.py", line 25, in <module>
    foo1(45)
  File "deco.py", line 17, in foo1
    return foo2(bar)
  File "deco.py", line 14, in foo2
    return foo3(bar)
  File "deco.py", line 11, in foo3
    return test(bar)
  File "deco.py", line 6, in wrapper
    traceback.print_stack(file=sys.stdout)
```

On a bien la trace de la stack d'appels jusqu'à l'appel de `test`

### 1.3.2

Ressource supplémentaire utilisée pour comprendre l'implémentation de décorateur via une classe

3. [http://www.artima.com/weblogs/viewpost.jsp?thread=240808]() et [https://www.artima.com/weblogs/viewpost.jsp?thread=240845]

L'objectif est de définir un décorateur, cette fois en utilisant une classe. Le comportement
désiré est le suivant : si la fonction 'bar' est présente dans la pile d'appel, on
affiche la trace de la pile, sinon on exécute simplement la fonction.

Fichier source pour cette question : `deco_class.py`

Le décorateur est définit via la classe `deco`:

```python
class deco(object):
    def __init__(self, name):

        #Name of the function we want in the call stack to print the stack trace
        self.name = name

    '''
    __call__ will be executed anytime the object 'deco' is called.
    fn will hold the reference to the function decorated. Each time this 
    function will be executed in the code, __call__ will be executed
    '''
    def __call__(self, fn):

        '''
        Defines the behaviour of the decorator. When the function referenced 
        by fn is executed, wrapper will be executed with the given parameters
        '*args' is used to be able to decorate functions with underdetermined 
        number of arguments.
        '''
        def wrapper(*args):

            #extract_stack() returns the call stack as a list of 4-tuples, 
            #in which the function name is given at index 2)
            stack_list = traceback.extract_stack()

            #We first check the call stack for a function named 'self.name'. 
            #If found, print the stack trace
            if self.isInStack(stack_list, self.name):
                traceback.print_stack(file=sys.stdout)

            #The function is called anyway
            fn(*args)
        return wrapper

    '''
    isInStack goes through the stack_list given in argument, and checks if the 
    function name given in argument is in it
    '''
    def isInStack(self, stack_list, fun_name):
        ret = False
        for s in stack_list:
            if s[2] == fun_name:
                ret = True
                break
        return ret
```

Les paramètres du décorateurs sont définis commes attributs d'instance. Ici, il
n'y a qu'un seul paramètre : `name`, c'est le nom de la fonction à chercher dans
la pile d'appel.

La fonction décorée sera la fonction `test`

```python
#This line decorates the function test, with "bar" as argument. It creates an instance of deco with attribute self.name = bar
#Each time test is called, the function __call__ of this instance will be executed.
@deco("bar")
def test():
    return "test function"

```

Le nom de la fonction à chercher dans la pile d'appel est passé en paramètre de
l'annotation définissant la décoration de la fonction.

Pour tester le comportement, la fonction `test` est appelée via deux chemins différents :
via les fonctions `fooX` successives, ce qui ne doit pas déclencher l'affichage de la 
trace, et via la fonction `bar`, ce qui doit bien évidemment déclencher cet affichage.

```python
'''
Functions used to call the decorated function 'test' through 
different call paths.
'''
def foo3():
    return test()

def foo2():
    return foo3()

def foo1(bar):
    return foo2()

def bar():
    return test()
```

Code de la fonction main : 

```python
if __name__ == '__main__':
    print "Calling foo1(). Should not print the stack"
    foo1(45)

    print "Calling bar(). Should print the stack"
    bar()
```

Résultat :

```
Calling foo1(). Should not print the stack
Calling bar(). Should print the stack
  File "deco_class.py", line 77, in <module>
    bar()
  File "deco_class.py", line 64, in bar
    return test()
  File "deco_class.py", line 31, in wrapper
    traceback.print_stack(file=sys.stdout)
```

Ce qui est le résultat attendu.

# 2 Introspection en Python

## 2.1

### Ressources

4. Doc Python sur les fonctions natives (dont font partie `dir()` et `globals()`) https://docs.python.org/2/library/functions.html

### Notes

Avant toute définition de fonction : 

* la fonction `dir()` retourne `['__builtins__', '__doc__', '__name__', '__package__']`
* la fonction `globals()` retourne `{'__builtins__': <module '__builtin__' (built-in)>, '__name__': '__main__', '__doc__': None, '__package__': None}`

La fonction `dir()` retourne la liste des *symboles* de l'objet passé en argument. Si aucun objet n'est passé en argument, elle retourne la liste des symboles du module courant.

La fonction `globals()` retourne un dictionnaire, représentant la table des symboles globaux du module dans lequel elle est appelée. La clé du dictionnaire est le nom du symbole, la valeur est la référence de l'objet que nomme le symbole.

Si on définit une fonction foo() de la manière suivante : 

```python
def foo():
    print "whatever"
```

La chaine de charactères `'foo'` est ajoutée à la liste retournée par `dir()` :

```python
['__builtins__', '__doc__', '__name__', '__package__', 'foo']
```

et l'entrée `'foo': <function foo at 0x7ff8837fd5f0>` est ajoutée au dictionnaire retourné par globals().

Si on ajoute une fonction `fooWithArgs(a)` :

```python
def fooWithArgs(a):
    return a + 2
```

On a exactement les mêmes modifications de `dir()` et `globals()`. On ne peut donc pas récupérer la signature complète d'une fonction uniquement en utilisant `dir()` et `globals()`.

## 2.2 isinstance et type

Fichier source `type.py`

### Ressources

5. Doc Python sur les types : https://docs.python.org/2/library/types.html?highlight=types#module-types


### Notes

* Remarque : itération sur un dictionnaire. Ne pas utiliser dictname.itername() quand le dictionnaire est modifié pendant la boucle. Il est préférable d'utiliser la méthode `keys()` pour obtenir la liste des clés, et itérer dessus.

Pour extraire seulement les fonctions du dictionnaire retourné par `globals()`, j'ai écrit la fonction suivante :

```python
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
```

Pour chaque clé du dictionnaire retourné par globals, on regarde si le type est `types.FunctionType` à l'aide de `isinstance(..)`, et si c'est le cas, on ajoute la paire (clé, valeur) au dictionnaire de sortie.

J'ai ai profité pour tester quelques comportements :

* Fonction interne : les fonctions internes ne sont pas des symboles globaux, et donc n'apparaissent pas dans le dictionnaire. (cf. `fooWithInner()`)
* Ordre des fonctions : seules les fonctiones définies avant **l'apel** de la fonction `getFunctions()` apparaissent dans le dictionnaire. La fonction `fooAfterGetFunction()` est présente, bien que définie après la définition de `getFunctions()`, mais la fonction `fooAfterMain()`, définie après l'appel de `getFunctions()`, n'apparait pas. Cela s'explique par le fait que la fonction `globals()` donne l'état actuel de la table des symboles, et au moment de l'appel de `getFunctions()`, `fooAfterMain()` n'est pas encore définie.

#2.3 Passage de parametres

Source : `params.py`

La fonction `wrap(fn, *args, **kwargs)` prend en premier argument la fonction à traiter, suivi des arguments nom només dans l'ordre, et enfin des arguments nommés. Elle affiche la valeur des arguments passés, et appelle la fonction passée en premier argument. Cette implémentation est déjà générale à mon sens, puisqu'elle passe les arguments à la fonction passée en argument, quelle qu'elle soit.

`*args` représente la liste des arguments non nommés. Attention, ce sont des arguments positionnels, ils doivent être passés dans l'ordre.
`**kwargs` représente la liste des arguments nommés, sous forme de dictionnaire. Les argument peuvent être passés dans le désordre, mais ces arguments doivent être placés après *tous* les arguments non nommés.

#2.4 Redéfinission de fonction à la volée

Source : `fun.py`

## Ressources

6. http://stackoverflow.com/questions/13503079/how-to-create-a-copy-of-a-python-function : Réponse stackoverflow sur la copie de fonction en python
7. https://docs.python.org/2/library/copy.html : Doc python sur le module copy
8. http://www.linuxtopia.org/online_books/programming_books/python_programming/python_ch10s04.html

## Notes

J'ai repris la fonction `foo(a, b, c)` du 2.3, et j'ai essayé de la copier, en vérifiant que la fonction copiée était différence de la fonction d'origine, avec un test d'assertion sur `g is not foo`.

Premier essai : 

J'ai voulu utiliser copier `foo` dans `h` avec `copy.deepcopy(foo)` (cf. ressource 7.), mais l'assertion `assert h is not foo` soulève une exception, et la représentation sous forme de chaine de caractère (donnée par `print str(foo)`) donnent la même référence.

J'ai trouvé la solution suivante sur stackoverflow :

```python
def copyFunction(f, f_name):
    return types.FunctionType(f.func_code, f.func_globals, name = f_name,
                            argdefs = f.func_defaults,
                            closure = f.func_closure)
[...]
g = copyFunction(foo, "g")
```

qui donne le résultat attendu: l'assertion `assert g is not foo` ne lève pas d'AssertionException, et les repésentations en chaine de charactères de `foo` et `g` sont différentes. 

J'ai cherché à comprendre cette solution, mais je n'ai pas trouvé de documentation pour le constructeur `types.FunctionType(..)`. La documentation du module `types` (cf. ref. 5.) définit simplement `types.FunctionType`, pas de fonction ayant le même nom. La référence 8. donne cependant quelques indices sur ce qui est effectué, en donnant des informations sur les attributs copiés : 

* `func_code` : le code de la fonction à copier
* `func_globals` : la table des symboles globaux de la fonction à copier, c'est à dire le dictionnaire retourné par `globals()` dans le module de définition de cette fonction
* `func_defaults` : les valeurs par défaut des arguments
* `func_closure` : le mécanisme qui permet de garder les symboles extérieurs que la fonction utilise (cf. 1.3.1)





