---
date: 2024-07-06
published: true
template: blog.html
---

# Microcorruption: Johannesburg

In this level we're dealing with the HSM-1 which only performs a password
check, but this time the code implements some bounds checks on the password. It
appears that this bounds check is happening after copying and checking for a
canary value `0x30` in the 18th byte of the input as offset between user input
and return address is 18 bytes this time instead of 16 bytes in the previous
levels. The solution is a 17 byte sequence of non-null characters followed by
the canary value the address of the `unlock_door` function.

Solution: `50505050505050505050505050505050ff304644`
