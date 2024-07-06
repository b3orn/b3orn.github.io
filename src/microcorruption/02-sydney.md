---
date: 2024-07-06
published: true
template: blog.html
---

# Microcorruption: Sydney

The `create_password` function from [New Orleans](01-new-orleans) has been
removed again, the password is now directly encoded into `cmp` instructions
in the `check_password` function. Each `cmp` instruction compares two bytes and
attention has to be paid to the order of bytes. The used MSP430 microcontroller
is little endian so the two hex encoded characters in the `cmp` instruction have
to be read from right to left, for example the first two bytes in

```
cmp	#0x3a2d, 0x0(r15)
```

encoded as `0x3a2d` are `0x2d` (-) and `0x3a` (:).


Solution: `-:OlTvMV`
