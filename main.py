import time
import jartex

count = 0

while True:
    print("Run Count: " + str(count))
    jartex.main()
    count += 1
    time.sleep(600)