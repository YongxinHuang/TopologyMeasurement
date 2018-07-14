Download traceroute data from https://atlas.ripe.net.
There are three steps for it.

step_one.py is download the file that RIPE's items.  step_one.py [time_start ,time_stop],e.g. python3 step_one.py 20180601 20180630
step_two.py is download the traceroute data from local items' files. step_two.py [time_start,time_stop] python3 step_two.py 20180601 20180630
analyzeResults.py use the official library to parse the original data. python3 analyzeResults.py rawdata.20180601 

