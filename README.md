# MyPassword
Save your password in an encrypted file

# How to use it
Needed: `pycryptodome`

1. fill "password" and "iv" in `init.py`, they are the passwords to open the encrypted file

2. run init.py to generate a password.json

3. run password.py to manage your password

# Structure
To create a save in your file, you should fill "host", "account", "password" and "note", where "note" is used for you to search this password sometime.

For example:
```bash
host: github.com
account: test
password: test
note: github code repository
```

# Note
When you run password.py, you should type in "password" and "iv" one by one
