#!/usr/bin/expect

set timeout -1

#Trocar pela sua senha, mas mantem o \r no final
set senha "Suasenhaaqui\r"

#Mesmo aqui, trocar pelo seu usuario e manter o \r
set eRaider "luccorte\r"

#Trocar luccorte aqui pelo seu usuario
spawn ssh luccorte@ssh.ttu.edu

expect "*assword: " 

send -- $senha

expect "SSH instance: " 

send -- "login.hpcc.ttu.edu\r"

expect "*?ser account to connect with: " 

send -- $eRaider 

expect "*?assword: " 

send -- $senha 

expect "*Current Storage * " 

#Eu normalmente logo numa sessao interativa pra poder usar o terminal sem medo de travar o login node:
send -- "interactive -p nocona\r"

#Ou logo no nocona como acima ou logo no matador:
#send -- "interactive -p matador\r"

#Se quiser ver como esta a situacao da fila assim que logar, descomenta essas 2 linhas abaixo
#expect "* ready for job*"

#send -- "squeue|grep matador\r"

interact
