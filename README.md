Traceback (most recent call last):
  File "/Users/tkrey/Desktop/Programmieren/ttt-main/main.py", line 113, in <module>
    main()
  File "/Users/tkrey/Desktop/Programmieren/ttt-main/main.py", line 61, in main
    game, conn = new_game(profile)
                 ^^^^^^^^^^^^^^^^^
  File "/Users/tkrey/Desktop/Programmieren/ttt-main/main.py", line 12, in new_game
    server = Server(game, profile)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/tkrey/Desktop/Programmieren/ttt-main/scripts/server.py", line 15, in __init__
    self.ip = socket.gethostbyname(socket.gethostname())
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
socket.gaierror: [Errno 8] nodename nor servname provided, or not known
