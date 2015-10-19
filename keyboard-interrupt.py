import time

print "sleeping..."
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print "\nThere was an interrupt!"
        print "Type 1 to continue or any other key to exit"
        x = raw_input()
        if x == "1":
            print "sleeping..."
            pass
        else:
            print "Exiting..."
            exit(0)
