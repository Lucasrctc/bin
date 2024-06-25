#!/usr/bin/expect

set timeout -1

set brachiosaurus "NQBGBLFJ4mzvH57yrK5vEyqSz\r"

set stegosaurus "luccorte\r"

spawn ssh luccorte@ssh.ttu.edu

expect "*assword: " 

send -- $brachiosaurus

expect "SSH instance: " 

send -- "login.hpcc.ttu.edu\r"

expect "*?ser account to connect with: " 

send -- $stegosaurus 

expect "*?assword: " 

send -- $brachiosaurus 

expect "*Current Storage * " 

#send -- "interactive -p nocona\r"

#expect "* ready for job*"

#send -- "cd Baryonyx/python;squeue|grep matador\r"

interact
