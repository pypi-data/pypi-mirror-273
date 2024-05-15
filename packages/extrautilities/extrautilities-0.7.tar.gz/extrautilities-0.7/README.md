# ExtraUtils
will provide a bunch of small functionalities to speedup developement.

(In active developement, so if you have any suggestions, to make other developers life easier, feel free to submit them.)

Currently ExtraUtils only has one feature.
### RateLimiter()
```py
# A very simplified example
from ExtraUtils import RateLimiter
rate_limit = RateLimiter(10,15,5,1,True)
# threshold (10) -> increments before rate_limit.hit is set to True
# upperCap (15) -> the highest value the trigger counter will go
# decay_rate (5) -> the amount in triggers to be decremented each decay cycle
# decay_time (1) -> the time in seconds between each decay cycle
# extreme_case (True) -> if a exeption should be raised (if True) or just rate_limit.hit set to True (if False)

def rate_limit_test(i:int):
    rate_limit.increment()
    print(i,rate_limit.hit)

for i in range(20):
    rate_limit_test(i)

# Output:	
#0 False
#(1 to 8) False
#9 False
#Traceback (most recent call last):
#  File "E:\Developement\RTS-Modules\ExtraUtils\showcase.py", line 14, in <module>
#    rate_limit_test(i)
#  File "E:\Developement\RTS-Modules\ExtraUtils\showcase.py", line 5, in rate_limit_test
#    rate_limiter.increment()
#  File "E:\Developement\RTS-Modules\ExtraUtils\ExtraUtils\RateLimit.py", line 30, in increment
#    raise RateLimited()
#ExtraUtils.RateLimit.RateLimited: Rate limit reached
```
Aditional methods are:
```py
RateLimiter().pause_decay()
RateLimiter().resume_decay()
```
