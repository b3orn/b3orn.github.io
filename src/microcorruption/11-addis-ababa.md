---
date: 2024-07-07
published: true
template: blog.html
---

# Microcorruption: Addis Ababa

The first main difference to the previous levels we notice in Addis Ababa is
the usage of `printf` in the `main` function. What is interesting about
`printf` here is that the user input is passed as the format string, which any
modern C compiler will warn you about as the attacker gets some control about
how data is read and written from and to the stack which is where normally the
variable number of arguments are located. Looking in the manual we can find the
`%n` option which writes the number of characters printed so far to the
provided memory address, with `%x` we can read an unsigned int (in thise case
16 bit/2 bytes) and with that advance a kind of stack pointer. Internally
`printf` reads the string given as the first argument partially onto the stack,
we can use that to write for example an address to the stack.  Another
interesting detail is that the username/password is printed after checking them
for validity in the `main` function and that it writes the result of the
password check onto the stack before calling `printf`, in case of mismatch it
writes a zero and if the password matches it writes some non-zero number. With
a well prepared input we can overwrite this value using `%n` and unlock the
door. Looking at the stack we need to move the "stack pointer" by 4 bytes, so
we need something like `%x%x`, with the second `%x` loading the target address,
alternatively we could use more `%x` to move the stack pointer so far that we
reach the full format string, which is also located on the stack.

Solution: `5555e63625782578256e` the `5555` is just padding.
