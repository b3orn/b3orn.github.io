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


Solution:

username = 16 * "77" + "9043" + "1624" + "b6fe"

password is unimportant
