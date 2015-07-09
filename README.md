# A collection of XMPP utils

`echobot.py` is a bot that just echoes back whatever message you send to it. Useful for testing purposes.

`sendxmpp.py` is the XMPP equivalent of sendmail. It is an alternative to the old sendxmpp written in Perl.

# Dependencies
 
 This requires Python 3.X
```
sudo apt-get install python3
```

Install dnspython
  ```
  wget https://github.com/rthalley/dnspython/archive/v1.11.1-py3.tar.gz

  tar xvf v1.11.1-py3.tar.gz
  
  cd dnspython-1.11.1-py3/
  
  sudo python3 setup.py install --record files.txt
  
  cd ../
  ```

Install SleekXMPP
 ```
 git clone https://github.com/fritzy/SleekXMPP
 
 cd SleekXMPP/
 
 sudo  python3 setup.py install
 
 cd ../
 ```

 Installation: just put the scripts wherever you want.
   

Configuration: see `CONFIG.example`, default config path is `~/.xmpputils`
```
cp CONFIG.example `~/.xmpputils
```
Edit `~/.xmpputils` with your xmpp credentials.

Usage: (assuming you're in xmpputils/)
```
 echo "This is a test" | ./sendxmpp.py user@host
```

