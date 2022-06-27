from suijisuosou_and_dafen import sjss_and_df
import time
for i in range(5):
    t0 = time.time()
    sjss_and_df()
    t1 = time.time()
    print(t1 - t0)
