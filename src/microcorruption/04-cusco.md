---
date: 2024-07-06
published: true
template: blog.html
---

# Microcorruption: Cusco

The HSM is still used but the exploit from the last level doesn't work anymore
as the return valud from `test_password_valid` is used as intended without any
weird writes and comparisons in reachable memory addresses. But this isn't the
only change, in the last level the user input was stored to an explicit address
far from the stack, this was changed and the user input is stored directly on
the stack. This is exploitable and with a well crafted input it is possible to
overwrite the return address of `login` to the address of `unlock_door`. In
this case the return address of `login` is stored at `0x43fe`, the user input
starts at `0x43ee`. A sequence of 18 bytes will overwrite the return address,
the last two bytes of this sequence are the address of `unlock_door` in reverse
order due to the little endianness of the MSP430. In this case the address of
`unlock_door` is `0x4446`, therefore the sequence should end with `0x46` "F"
and `0x44` "D".

Solution: Any 18 character sequence ending in `FD`.
