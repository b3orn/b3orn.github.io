---
date: 2024-07-06
published: true
template: blog.html
---

# Microcorruption: Reykjavik

Unlike the last two levels this one doesn't use the HSM. The actual code is
obfuscated by being encoded in some way, it will be decoded using the `enc`
function. The manual calls this "military grade encryption", which means it was
made by the lowest bidder and should be easily breakable. The decoded code will
be stored at `0x2400` and is 248 bytes long, fortunately Microcorruption
provides a disassembler, but no labels or correct memory addresses are provided
which makes this just slightly harder and take somewhat more time. The code
contains two functions the first will be called `login` and the second appears
to be responsible for interrupt handling, being used to output characters, read
input from the user and unlock the door. The `login` function will first prompt
for a password and then compares with a constant:

```
2448: b490 d077 dcff cmp	#0x77d0, -0x24(r4)
```

Keeping in mind that we're dealing with a little endian microcontroller we set
the input mode to hex and enter the two bytes in reverse order, that is `D077`

Solution: `D077`

Appendix: [Disassembled deobfuscated code](05-reykjavik.s)
