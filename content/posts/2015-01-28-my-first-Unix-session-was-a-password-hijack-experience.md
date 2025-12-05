---
title: My first Unix session was a password hijack experience
date: 2015-01-28
aliases:
- /2015/01/28/my-first-Unix-session-was-a-password-hijack-experience
---

![VT220 terminal - Photo under Public Domain license by Shansov.net / Wikimedia](https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/DEC_vt220.jpg/1920px-DEC_vt220.jpg)


I discovered Unix (not Linux) at college in Bordeaux, in 1989. After a first course about Unix and its concepts, our professor gave us our credentials to be able to login on our school Unix system.

This computer was a [HP 9000 server](https://en.wikipedia.org/wiki/HP_9000#Server_models) running a Unix OS. The "machine room" was in fact divided in two rooms. The first one was the "white room", a restricted access area with only the big box inside aka the main server : 1,5m high and several meters long. The second room was the room dedicated to the twenty passive terminals (VT100/VT220 emulation maybe) used to login on the Unix system.

So, with my user account and password, I sat in front of one of the terminals. I entered my user account and my password. **Failed**. I just thinked that I mispelled one of them, I retried and I managed to log in. The rest of the session was successful : I was able to try the few commands I learned during my first lesson.

But. The day after, I was not able to log in anymore. 2nd year students were just laughing in the terminals room. I asked why. They stopped laughing, picked a terminal and introduced me to the **.logout functionnality**. It is used to execute a set of commands when you leave your current session. They have customized their own .logout script in order to display a screen almost identical to the normal login screen.

**Yes, you see?** My first try to enter my credentials the day before was done on a **faked login screen** ;-) The student who was connected before me got my credentials and just has to change my password. After getting my credentials, the commands executed by the .logout script ended and the student session also. So I retried to enter my credentials in front of the real login screen.

It was in 1989. On a Unix system. Connected to ... nothing : no network available at this time on this server. And password theft was already a game :-)
