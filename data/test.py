import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# this is how the data will be structured
trace_format = [
    'Event_Type', 
    'Time', 
    'Src_Node', 
    'Dst_Node', 
    'Pckt_Type', 
    'Pckt_Size', 
    'Flags', 
    'Flow_Identifier', 
    'Src_Address', 
    'Dst_Address', 
    'Pckt_Number', 
    'Pckt_Identifier']

df_trace = pd.read_csv('trace_file.res', sep=' ', names = trace_format) # importing the data into a pandas.dataframe
df_trace.head() # show first 5 rows

df_trace.info() # get dataframe info, to see if its needed to clean

metrics_format = [
    'Time',
    'rtt',
    'srtt', 
    'cwnd', 
    'cwmax', 
    'bo',
    'rto',
    'cw'] # values collected

df_metrics = pd.read_csv('congestion_window.res', sep=' ', names = metrics_format)
df_metrics.head()

lost_pckts = df_trace.Event_Type == 'd' # get lots packets by mapping those ones with event_type == 'd' (dropped)
ids = df_trace[lost_pckts].Flow_Identifier # filter by the flow_identifier (class)
# we could also filter by Src_Address, as we need the packets dropped by the n3

n0_lost = sum(ids == 0) # TCP Tahoe
n1_lost = sum(ids == 1) # TCP Reno

print("Lost Packets")
print("Node 0, TCP Tahoe:\t", n0_lost)
print("Node 1, TCP Reno:\t", n1_lost)
print("Total: ", ids.count())

cwnd0 = df_metrics.cwnd
time = df_metrics.Time
rto = df_metrics.rto
cw = df_metrics.cw
plt.figure(figsize=(12,8))
plt.plot(time, cwnd0, color='blue')

plt.title('Congestion window x Time')
plt.xlabel('Time (s)')
plt.ylabel('Congestion window (MSS)')
plt.legend(loc='upper right')
plt.savefig("cwnd-plot.png")
plt.show()


plt.figure(figsize=(12,8))
plt.plot(time, cw, color='blue')

plt.title('CW x Time')
plt.xlabel('Time (s)')
plt.ylabel('Timeout Congestion')
plt.legend(loc='upper right')
plt.savefig("cw-plot.png")
plt.show()


