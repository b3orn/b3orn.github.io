---
date: 2024-07-06
published: true
template: blog.html
---

# Microcorruption: Whitehorse

In this level we're dealing with the HSM-2 which unlocks the door directly
instead of just providing a password check functionality, this might complicate
things. The core logic is in the `login` function and the password is again
written to the stack, which might be exploitable. The door is conditionally
unlocked by the HSM in the `conditional_unlock_door` function, but all we need
from that is the address at which the interrupt handler is called. The manual
tells us that the deadbolt is still connected to the microcontroller, by
writing the necessary information on the stack we should be able to unlock the
door, circumventing the HSM. The return address is exactly 16 bytes from the
location where the password starts. The input has to be 22 bytes long, first we
put 16 bytes of random data as padding on the stack followed by the address of
the interrupt handler `0x4532`, followed by two bytes of padding and finally
the interrupt code to unlock the door `0x7f`. The interrupt handler address has
to be put as `3245` in the input string to account for the endianness, the
input should end with `324500007f`

Solution: `50505050505050505050505050505050324500007f`
