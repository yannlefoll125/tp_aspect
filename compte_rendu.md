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




