# lanchat

a tiny chat app that lives on your local network.

no account
no cloud
no database
no internet

just wifi and python.

## how it works

one computer runs the server. everyone else joins it.

the client uses a little udp broadcast to find the server, then switches to tcp for the actual chat.

## running it

you need python 3.11+.

start the server:

python server.py

then on another computer on the same network:

python client.py

if discovery is being annoying, connect directly:

python client.py 192.168.1.42

## commands

- /help
- /who
- /name yourname
- /quit

## ports

- tcp 42691 for chat
- udp 42690 for discovery

if windows firewall asks about python, allow it on your private network.

## little roadmap

- file drops
- typing indicators
- message history
- rooms
- better terminal ui
- maybe encryption

built mostly because i thought it would be funny to have a chat app that doesn't need the internet.
