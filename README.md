# chat-clients

This code was written to complete an assignment for CS:3640, Introduction to Networks and 
Their Applications at the University of Iowa during the Spring 2025 semester. After learning
about the transport layer in the layered architecture of networks, I was responsible for 
implementing communication between devices in Python code. There are two different 
approaches to end-to-end communication in the transport layer and both are demonstrated here.
The first way only uses UDP with communication solely between the two clients which is shown in chat.py. 
The second model in client2.py still uses UDP to communicate with each other but additionally 
implements TCP so that the clients can talk with a directory server. 
