---
date: 2024-07-07
published: true
template: blog.html
---

# Microcorruption: Jakarta

Jakarta features the HSM-1 again and we need a uername and password, which
together may not be more than 32 characters. Most of the logic is in `login`
with the HSM being called in `test_username_and_password_valid`. After entering
the username it is copied to the stack using `strcpy`, then it's length is
calculated and compared to `0x21` (33), it the length is larger the program
terminates. For the password the length is limited to `0x1f` (31) minus the
length of the username, after copying the password to the stack its length is
also calculated, added to the length of the username and then compared again to
`0x21` (33). The important part here is that the comparisons only compare one
byte, with an input long enough it should be possible to create an integer
overflow. The input length of the username is limited to 255 characters, so we
need to look at how the password is handled. The password length limit is 31
minus the length of the username, the username is limited to 32 characters,
by using this as the username length we create an integer underflow and the
permissible password length is now 511 characters. If the username has a length
of 32 characters then if the password is 224 characters long the total length
is 256 characters which leads to the lower byte to be zero, which is less than
33 and therefore the program doesn't terminate. All that remains is to craft an
input that will unlock the door. The return address is at an offset of 36
characters from the location of the username on the stack, as we choose the
username to be 32 bytes long for the underflow to work (other lengths work too)
the new return address has to be part of the password which is copied directly
at the end of the username. Therefore the return address which is the address
of `unlock_door` has to be the fifth and sixth character in the password, in
this case `LD`.

Solution:

username = 32 non-null characters, e.g. four times `USERNAME`

password = 4 characters followed by `LD` followed by 218 characters
