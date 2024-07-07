---
date: 2024-07-07
published: true
template: blog.html
---

# Microcorruption: Santa Cruz

Another level featuring the HSM-1, but this time we need a username and
password, both are between 8 and 16 characters long. After entering the
username it will be copied to the stack, then we enter the password which will
also be copied to the stack in the `login` function. There is also a function
named `test_username_and_password_valid`, but for some reason that function
is never called and all the logic including calling the HSM is in `login`. The
username and password are both copied using `strcpy` without any limitation of
the input length, despite the stated limitations. The length of the password is
determined after copying it to the stack, if it is longer than 15 characters
the program ends, interestingly that doesn't match what the output of the
program states. If the password is shorter than 8 characters the program also
terminates. There is no bounds check for the username, the username is copied
before the password and if the username is "too long" the password will
overwrite parts of it. At specific addresses on the stack the program stores
the minimum and maximum length of the password as well as a null byte that is
checked at the end of the `login` function, if this bytes is not null the
program will terminate without reaching the `ret` instruction. Since `strcpy`
stops copying at a null-byte we can't have any null-bytes in the username or
password, but we can manipulate the maximum length of the password and use
the null termination of it to insert a null byte at the desired location. The
total length of the username is 44 bytes and ends with the address of the
`unlock_door` function. The password starts 19 bytes after the username, the
null-byte is located 36 bytes after the start of the username, therefore the
password has to have a length of 17 characters, the minimum length is located
at an offset of 17 bytes and the maximum at 18 bytes from the start of the
username.

Solution: username in hex, password in plain text

username = `5555555555555555555555555555555555082055555555555555555555555555555555555555555555554a44`

password = `PASSWORDPASSWORD1` (any 17 character long string)
