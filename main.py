import time
import jartex

count = 1

while True:
    print("Run Count: " + str(count))
    jartex.main()
    count += 1
    #Run every 300 seconds/5 minutes
    time.sleep(300)