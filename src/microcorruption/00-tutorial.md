---
date: 2024-07-06
published: true
template: blog.html
---

# Microcorruption: Tutorial

Function `check_password` sets `r15` to `1` on success or `0` on failure. The
function counts characters until a null byte is found, the number of bytes
including null bytes is stored in `r12`. It then compares `r12` to `9` using
the `cmp` instruction which sets the zero flag in case of equality, address
`0x448e`. If the zero flag is set, i.e. a string of eight characters is entered
(a null byte is added to the sequence), `r15` is set to one and the door
unlocks.

Solution: Any 8 byte sequence
