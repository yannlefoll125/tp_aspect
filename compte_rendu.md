# Partie 1

## 1.1 PATH

Initialement, `wc` appelle `/usr/bin/wc` (comme indiqué par le résultat de `which wc`)

Mon script bash *wc* affiche "hi", puis appelle *wc* en lui passant l'ensemble des arguments.

Pour appeler mon script lorsque j'appelle wc dans un terminal, je l'ajoute au path
```
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
```
LD_PRELOAD=./hack.so ./hello
```

* Remarque : Dans un premier temps, j'ai implémenté mon `puts` en utilisant `printf`. Mais comme `printf` est remplacée par `puts`, j'appelais récursivement ma propre implémentation de `puts` (même erreur que pour le 1.1). J'ai donc implémenté mon `puts` avec l'appel système `write`

## 1.3 Décorateurs Python



