# login-tracker
Student computer login tracker for teachers and administrators.


The idea is to have a centralized server in which all logins to a computer in a network will be tracked, along with a programme running on a teacher's PC to keep track of who's connected in a given classroom/labratory. Logs of logins are saved on all of the three devices (the student PC, the teacher's PC and the main server.).


Everything is optional so you can have both no mainServer or teacher's machine turned on, or you can have either one running, everything is still going to get logged in the running machines.

The client software prevents the task manager from running, block keys such as alt,f4,tab etc. , disables explorer.exe while you're not logged in. 

## How to use

- Edit configuration settings for each file
  - Set only ports for mainServer and newServer.
  - For the client configuration set the ip and port for both the teacher's PC and the main server.
- Run the mainServer on your server to keep track of all logins on PCs in a centralized place.
- Run newServer on the teacher's PC to keep track of connected users. 
- Run the client on all PCs.
- On the teacher's window you can hit the "Lock" button to lock all connected PCs.
- Change background.png to whatever u wish.
 
 ## Development
 - Tested with Python version 3.11.1
 - run `pip install -r requirements.txt` to install the dependencies.
 - Compile to exe with `python -m pyinstaller --noconsole <file>.py`.
 Compiling it as a standalone file might trigger an antivirus, so it's safer to compile it in one directory.
