---
date: 2024-07-06
published: true
template: blog.html
---

# Microcorruption: New Orleans

In this exercise the `check_password` function performs a comparison with
another string stored at `0x2400`. At the start of the `main` function, before
any user input, the function `create_password` is called which writes a
hardcoded string into memory at address `0x2400`. The solution can be either
read from the code of the `create_password` function or from memory.

Solution: `*;sA(*]`
