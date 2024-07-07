---
date: 2024-07-07
published: true
template: blog.html
---

# Microcorruption: Novosibirsk

Unlike [Addis Ababa](11-addis-ababa), Novosibirsk features an HSM-2, which
unlooks the door itself. The exploitable use `printf` is still present, but
HSM-2 doesn't write anything to memory and `printf` is called before the
validation of the password. It appears we can overwrite the code, with that
we can write a different interrupt code into the `conditional_unlock_door`
function to unlock the door instead of calling the HSM.

Original code:

```
44c6:  3012 7e00      push  #0x7e  ; call hsm-2
44ca:  b012 3645      call  #0x4536 <INT>
```

Manipulated code

```
44c6:  3012 7f00      push  #0x7f  ; open door
44ca:  b012 3645      call  #0x4536 <INT>
```

To achieve this we need to write `0x007f` to `0x44c8`, in other words we need
`printf` to write 127 characters and then write that number to the correct
address using `%n`. The `printf` function behaves slightly different, we need
to first provide the address then 125 characters to get the number of written
characters to the number we want to write to memory and then we use `%n` to
write to memory.

Solution: `c844` followed by 125 non-null characters followed by `256e`.
