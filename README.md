# CSI4999 - Smart Lock

## Welcome to Senior Capstone Project

## Smart Lock

### System Architecture
Smart Lock is a three application system to offer a wide range of functionality.

__Lock Controller__

The lock controller is handled by a Raspberrry Pi using it's GPIO interface to power a 5v Relay. The Raspberry Pi also acts as our BLE transmission beacon for our mobile application and back up entry via an onscreen keypad and persistent storage incase phone is dead or forgotten.

__Web Management__

Our web application allows users to manage who has access to it's lock aswell as to other user account settings.
http://adsanvar.pythonanywhere.com


__Mobile Application__

*Android*

The sole purpose for this application is to provide a passive unlock to the user when hands our occupied. This is implemented using BLE to transmit a signal with a specific ip to handshake and share information between Mobile and Raspberry Pi.
