---
date: 2024-07-06
published: true
template: blog.html
---

# Microcorruption: Montevideo

We're again dealing with an HSM-2 which unlocks the door directly, but the
deadbolt is still connected to the microcontroller. The core logic is again
located in the `login` function, the password is no longer directly written to
the stack but after writing the input to the memory it is copied to the stack,
again without any bounds check. We can use the solution from
[Whitehorse](06-whitehorse) with slight adaptation, we need to change the
address of the interrupt handler, in my case to `0x454c`, and the padding
between return address and the interrupt code (normally the return address
of the interrupt handler) has to be non-null, otherwise `strcpy` will stop
there, for good measure we could add a null-byte at the end to make `strcpy`
not run into an endless loop, but the memory area the password is written to
is already nulled, so this is optional.


Solution: `505050505050505050505050505050504c45ffff7f00`
