# Import some necessary libraries.
import socket 
import ctypes
import time
import random
import re

# Some basic variables used to configure the bot        
server = "irc.freenode.net" # Server
channel = "#jacked" # Channel
botnick = "PokemonTest%d" % random.randint(1,10000) # Your bots nick


def ping(): # This is our first function! It will respond to server Pings.
  ircsock.send("PONG :pingis\n")  

def sendmsg(chan , msg): # This is the send message function, it simply sends messages to the channel.
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n") 

def joinchan(chan): # This function is used to join channels.
  ircsock.send("JOIN "+ chan +"\n")

def hello(): # This function responds to a user that inputs "Hello Mybot"
  ircsock.send("PRIVMSG "+ channel +" :Hello!\n")

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def aPress():

  PressKey(0x5A) # A key which is Z for emulator
  ReleaseKey(0x5A)

def bPress():
  
  PressKey(0x58) # B key which is X for emulator
  ReleaseKey(0x58)

def upPress():

  PressKey(0x26) # Up on DPad which is Up Arrow for emulator
  ReleaseKey(0x26)

def downPress():

  PressKey(0x28) # Down on DPad which is Down Arrow for emulator
  ReleaseKey(0x28)

def leftPress():

  PressKey(0x25) # Left on DPad which is Left Arrow for emulator
  ReleaseKey(0x25)

def rightPress():

  PressKey(0x27) # Right on DPad which is Right Arrow for emulator
  ReleaseKey(0x27) 

def startPress():
  
  PressKey(0x56) # Start key which is V for emulator
  time.sleep(2)
  ReleaseKey(0x56)

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :This bot is a result of a tutoral covered on http://shellium.org/wiki.\n") # user authentication
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot

joinchan(channel) # Join the channel using the functions we previously defined

IRC = "#jacked "

def printCommands(name, command):
  spaces = ""
  spaceBetween = 25 - (len(name)+len(command))
  while spaceBetween >0:
    spaces += " "
    spaceBetween -= 1
  print name+spaces+command


while 1: # Be careful with these! it might send you to an infinite loop
  ircmsg = ircsock.recv(2048) # receive data from the server
  ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
  #print(ircmsg) # Here we print what's coming from the server

  input = ircmsg
  expression = ':(.+)!.+ PRIVMSG #(.+) :(.+)'
  output = re.search(expression, input)

  if output:
    name = output.group(1)
    command = output.group(3)

    if ircmsg.find(":Hello "+ botnick) != -1: # If we can find "Hello Mybot" it will call the function hello()
      hello()

    if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
      ping()

    if command == "a": # Finding messages
      aPress()
      printCommands(name, command)

    if command == "b": # Finding messages
      bPress()
      printCommands(name, command)

    if command == "up": # Finding messages
      upPress()
      printCommands(name, command)

    if command == "down": # Finding messages
      downPress()
      printCommands(name, command)

    if command == "left": # Finding messages
      leftPress()
      printCommands(name, command)

    if command == "right": # Finding messages
      rightPress()
      printCommands(name, command)

    if command == "start": # Finding messages
      startPress()
      printCommands(name, command)

# Keyboard Commands
