---
date: 2024-07-10
published: true
template: blog.html
---

# Microcorruption: Algiers

The Algiers level doesn't contain `printf` anymore, but introduces `malloc` and
`free`. The `login` function allocates two buffers using `malloc` to store the
username and password, both buffers have a size of 16 bytes, but `getsn` which
is used to get the user input is limited to 48 bytes. Only the second input,
the password is passed to the `test_password_valid`, based on it's return value
the door is unlocked using `unlock_door`. Besides the usage of `malloc` and
`free` there is nothing obviously vulnerable in `login` and
`test_password_valid`. The `malloc` function stores information for each
allocation in front of the allocated memory, due to the higher input limit than
the allocated size we should be able to overwrite some of that information of
the second allocation and make free behave in some unintended way to write to
an address we supply, for example to overwrite a return address. There is a
total of six bytes between the end of the username memory and the beginning of
the password memory which contains information that is read by `free` and
partially written back to memory in order to merge previously allocated memory.
The structure in memory appears to be a pointer to the previous allocation, to
the next allocation and the size and a flag to mark an allocation as freed. The
exploit requires the knowledge of the location of the return address `0x4394`
which we will use to overwrite the the address of the previous allocation but
need to subtract 4, we  also need the original return address `0x46a8` and the
desired return address, i.e. the address of `unlock_door` which is `0x4564`,
from that we can calculate the value with which we need to overwrite the flags
as `unlock_door - 0x46a8 - 6 = 0xfeb6`.


Solution 1:

username = 16 * "77" + "9043" + "1624" + "b6fe"

password is unimportant


I think there should be a better solution that requires less knowledge of.
Theretically we could just write 16 random bytes then the address where we want
to go and then the location of the return address, but this will overwrite some
of the code at the target location we want to go to. Specifically these lines:

```
451a:  2e4f           mov   @r15, r14
...
4534:  1d4f 0200      mov   0x2(r15), r13
4538:  8d4e 0000      mov   r14, 0x0(r13)
```

The main problem with this approach is that control flow in `free` depends on
the values stored at the address we want to go to, over which we only get
control if we inject code. The "previous" address should be set to where we
locate our code, which will be the beginning of the username `0x240e`, and the
"next" address should be the location of the return address of `free`, in this
case `0x4394`. Due to the overwriting the first three words become useless and
in my opinion this is unavoidable. Without too much knowledge we have to brute
force some code that doesn't cause too much interference, no jumps, no
modifications of the `pc` register and so on, additionally we need an even
value at the flag offset, otherwise nothing gets written the way we want. The
code that I finally injected was:

```
mov  #0x1010, 0x2(r6)
call #0x4564
```

The `mov` instruction is three words long and is corrupted to `clr 0xe(r6)`
which causes no problems.


Solution 2:

username = "b64010100200b01264457777777777770e249443"

password is unimportant
