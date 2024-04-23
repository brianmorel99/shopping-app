# Shopping Cart App with Socket Programming

This is a simple shopping cart application for CSIS 501.  It is written in python and utilizes socket based programming with both TCP and UDP connections.
Includes Shopping-Cart-Screenshot.PNG which is for my teacher to see examples of invalid and valid login.

## Getting started

You will need three terminal / shell sessions to run this software.  It has only been tested on Linux, but should work on Windows.

You will need to extract the files from archive, or download from git via the below command.

```shell
git pull https://github.com/brianmorel99/shopping-app.git
```
Either way, change into the directory created in all three terminal / shell sessions

```shell
cd shopping-app
```

You then can start the server-1, server-2, and client each in their own terminal / shell.

```shell
python3 server-1.py
```

```shell
python3 server-2.py
```

```shell
python3 client.py
```

All interaction will then be from client.py.

# Login Data / CC Data

There are three files for helping create test users, test credit cards, and the encryption keys.

You do not need to run these files, as the files they output are already stored in the repository for use.

## makeCC.PY       
* This is for creating the text file that the program validates CC against.  The txt file has hashed version, so it's not directly readable.  The file contains the un-hashed versions, and they are reproduced below:
    * CC #: 0000000000000000
        - Exp.: 12/25
    * CC #: 1234567890123456
        - Exp.: 78/90
    * CC #: 1111111111111111
        - Exp.: 11/11

## makeKey.py
* This is for creating the shared symmetric encrption keys.
    - One key is created for communication between client and server-1
    - One key is created for communication between server-1 and server-2

## MakeUsers.py
* This creates the text file to validate the username & password to login.  The password is hashed in the text file, but the un-hashed versions are in this file, and reproduceed below.
    * Username: brian
        - Password: morel
    * Username: bmorel
        - Password: mypass
    * Username: teacher
        - Password: easy

