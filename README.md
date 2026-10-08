# lanchat

a tiny terminal chat app that lives on your local network.

no account  
no cloud  
no database  
no internet

just wifi and python.

## what this actually does

lanchat lets multiple computers on the same local network chat with each other from the terminal.

one computer runs the server.

everyone else runs the client.

the client can automatically find the server using a udp broadcast. once it finds the server, the actual chat uses tcp.

so basically:

```
computer 1
   |
   |  python server.py
   |
   +------ same wifi ------+
   |                       |
computer 2              computer 3
python client.py        python client.py
```

the server handles connected users and sends messages to everyone.

## requirements

you need:

- python 3.11 or newer
- windows, linux, or macos
- two or more computers for a real lan test
- all computers connected to the same local network

you do **not** need:

- pip
- node
- npm
- a database
- an account
- an api key
- internet access

there are no third party python packages right now.

## download the project

clone it:

```bash
git clone https://github.com/tavish22/lanchat.git
cd lanchat
```

or download the repo as a zip from github and extract it.

## easiest way to test it

you can test everything on one computer first.

### terminal 1 - start the server

open a terminal inside the lanchat folder:

```bash
python server.py
```

you should see something like:

```
lanchat server running on port 42691
waiting for people...
```

leave this terminal open.

### terminal 2 - join locally

open another terminal in the same folder:

```bash
python client.py 127.0.0.1
```

you should get a guest name and a prompt:

```
you are guest1
type /help for commands

>
```

type a message.

because there is only one client, you won't see the message come back to yourself yet. the server is still running and accepting connections.

### terminal 3 - join again

open a third terminal:

```bash
python client.py 127.0.0.1
```

now you have two clients connected to the same server.

send a message from one.

the other should receive it.

## real lan test

this is the part lanchat was actually made for.

you need two computers connected to the same wifi/router.

### computer 1 - server

open the project folder and run:

```bash
python server.py
```

leave it running.

### computer 2 - client

open the same project on the second computer and run:

```bash
python client.py
```

the client will say:

```
looking around for lanchat...
```

then it should find the server automatically:

```
found it at 192.168.x.x:42691
```

and connect.

that's it.

### computer 3, 4, 5...

run the same command on every other computer:

```bash
python client.py
```

everyone should end up in the same chat.

## if automatic discovery doesn't work

sometimes windows firewall, router settings, guest wifi, or network isolation can block udp broadcasts.

don't panic.

first find the server computer's local ip address.

### windows

on the server computer:

```bat
ipconfig
```

look for something like:

```
IPv4 Address. . . . . . . . . . . : 192.168.1.42
```

then on the client computer run:

```bash
python client.py 192.168.1.42
```

replace the ip with the actual address of the server.

### linux

run:

```bash
ip addr
```

or:

```bash
hostname -I
```

then use the local ip with:

```bash
python client.py YOUR_IP
```

### macos

run:

```bash
ipconfig getifaddr en0
```

if you're using another network interface, you may need to check `ifconfig`.

then:

```bash
python client.py YOUR_IP
```

## windows firewall

windows may show a firewall popup the first time you run the server.

allow python through the firewall on **private networks**.

if you accidentally blocked it, open:

```
Windows Security
-> Firewall & network protection
-> Allow an app through firewall
```

make sure python is allowed on private networks.

don't randomly disable your firewall just to make the app work.

## ports

lanchat uses two ports:

| port | protocol | used for |
|---|---|---|
| 42691 | tcp | actual chat |
| 42690 | udp | finding the server |

these are local network ports.

the app doesn't need port forwarding on your router.

you should **not** expose lanchat to the public internet.

## changing the ports

you can change the chat and discovery ports with environment variables.

chat port:

### windows cmd

```bat
set LANCHAT_PORT=50000
python server.py
```

### powershell

```powershell
$env:LANCHAT_PORT="50000"
python server.py
```

discovery port:

### windows cmd

```bat
set LANCHAT_DISCOVERY_PORT=50001
python server.py
```

### powershell

```powershell
$env:LANCHAT_DISCOVERY_PORT="50001"
python server.py
```

if you change the discovery port, every client/server needs to use the same setting.

## commands

once you're inside the chat:

### change your name

```
/name tavish
```

### see who's online

```
/who
```

### see the commands

```
/help
```

### leave

```
/quit
```

anything that isn't a command gets sent as a chat message.

## project structure

```
lanchat/
├── client.py
├── server.py
├── discovery.py
├── protocol.py
├── config.py
├── ui.py
├── test_protocol.py
├── start_server.bat
├── requirements.txt
├── .gitignore
└── README.md
```

### client.py

the terminal client.

it connects to the server, reads input, sends messages, and listens for messages from other people.

### server.py

the main chat server.

it accepts tcp connections, keeps track of users, receives messages, and broadcasts them to everyone.

### discovery.py

handles the little udp broadcast used to find a lanchat server automatically.

### protocol.py

handles the message format used between clients and the server.

messages are length-prefixed json packets so tcp knows exactly where one message ends and the next one begins.

### config.py

keeps the basic settings in one place.

### ui.py

handles the terminal output and timestamps.

### test_protocol.py

a small test for the packet system.

run it with:

```bash
python test_protocol.py
```

you should see:

```
protocol test passed
```

## how the networking works

there are two parts.

### 1. discovery

the client sends a udp broadcast:

```
255.255.255.255:42690
```

the server listens for the discovery message and replies with its tcp port.

this means you don't normally need to know the server's ip beforehand.

### 2. chat

after discovery, the client connects to the server using tcp:

```
server-ip:42691
```

tcp is used for chat because we don't want messages randomly disappearing or arriving in the wrong order.

the server then keeps a connection open for each client.

## troubleshooting

### "couldn't find a server"

try connecting directly:

```
python client.py SERVER_IP
```

also check:

- both computers are on the same wifi
- you're not using guest wifi
- windows firewall allows python
- the server is actually running
- the server ip is correct

### "connection refused"

the server probably isn't running, the ip is wrong, or the chat port is blocked.

start:

```
python server.py
```

then try again.

### "address already in use"

something is already using port 42691.

either stop the other lanchat server or choose another chat port.

### clients can connect locally but not from another pc

that's usually a firewall/network issue.

first try:

```
python client.py SERVER_IP
```

if that still fails, check the firewall and make sure both machines are actually on the same local network.

### wifi is weird

some school, hotel, public, and guest networks intentionally prevent devices from talking to each other.

lanchat can't bypass that.

## security

this is a local-network project, not a production messaging service.

messages are not end-to-end encrypted.

there is no login system.

there is no authentication.

anyone who can reach the server can potentially connect.

don't run it on an untrusted network.

also don't port-forward the chat server onto the internet.

## development

there are no dependencies to install right now.

so you can just run:

```bash
python server.py
```

or:

```bash
python client.py
```

run the protocol test with:

```bash
python test_protocol.py
```

## roadmap

stuff that could be added later:

- file drops
- typing indicators
- message history
- chat rooms
- better terminal ui
- user colors
- private messages
- reactions
- encryption
- server commands
- kick/mute controls
- tiny file sharing
- maybe voice chat if we get stupid enough

## why i made this

because making another todo app felt boring.

i wanted something that actually touches networking, sockets, protocols, threading, discovery, and terminal stuff.

and now two computers on the same wifi can yell at each other without the internet.

pretty sick honestly.
