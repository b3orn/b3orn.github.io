---
date: 2024-07-06
published: true
template: blog.html
---

# Microcorruption: Hanoi

This level introduces a hardware security module (HSM). The `main` function
only calls the `login` function, which prompts for a password and reminds us
that passwords are between `8` and `16` characters long. The entered password
is stored at `0x2400` and he password validation happens in the
`test_password_valid` function, but looking at the code of this function it
appears that there's not much to exploit here at the moment. Once
`test_password_valid` returns `r15` is checked, if it is
not `0` the memory at address `0x2410` is set to `0x69`, it's not entirely
clear what the intention of that is, as a few instructions later that very same
memory address is compared to a value, `0x29` also known as `)` in my case (I
think these can vary from player to player), the memory location is exactly 16
bytes above the address where the password is stored and the password length
is never checked at the input so we can just enter any 17 character long
sequence with the last character being `)` and we're in.

Solution: 17 character string with last character being  `)`
