# Client-Server-Project-in-Python

Implementation of a TCP client-server with multithreaded file sending and receiving

The project includes a TCP client-server implementation developed with a python language. In it, you find a client that can request a file next to the TCP server that serves the requested file. After the client establishes a connection with the requested server, it sends the filename. When the server requests memory, it looks for the file in the file manager in its archive. If the file is found anywhere, the server will pass or the contents of the file to the client over the same connection.
The operational modules used are not the ones that present the project and protocol with the aim of using the Python system, the Socket that is to send data from the network structure that implements binaries to serialize and deserialize a network that is mainly with the configuration of a script that works as a current run of execution used to do the tasks form a script that works like your current application. When establishing the connection with the client, the server starts the list waiting for your request, which can be: List of files present in the server's cache for this purpose a program function was created, in addition to when closing a request the server sends a message with the names of the files that have been allocated in the server cache.
Initially, the server checks if the requested file is allocated in its cache memory. If so, the file payload goes through the deserialization process, followed by sending it to the client. When finished, the connection is closed. If the requested file is not in the server's cache memory, we have some situations:

If the file exists on the server and the file size is larger than the cache, the server will send the file to the client and terminate the connection. Otherwise, the server opens the file according to the specified buffer size and sends it. At the end of the submission, the server serializes and caches the file's payload to serve the file faster in subsequent queries.
During the payload storage stage of the file, check for free space in cache memory, which is limited to 64 MB. If the size of the file in question exceeds the limit value of the cache memory, there is a process of reallocation of the file present in the cache.
One strategy that used to be a relocation process was to check the cache memory of any file larger than the requested file, delete that file, and store the new file. If none of the files are larger than requested, the file delete loop will continue until the cache has enough space to allocate a new file.

Program Operation
1. To perform the file request, the client must provide the following input:
python3 client.py host port filename directory.
2. To request to view the files in cache memory, the client provides the following input:
python3 client.py host port list
3. To perform the server initialization, you must meet the following entry:
4. python3 server.py host port filename directory.
