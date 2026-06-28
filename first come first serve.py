#first come first served is a CPU scheduling algorithm. processes are executed in the oder they arrive with no preemption.
def fcfs(processes):
    print("\n--- FCFS CPU Scheduling ---\n")
    print(f"{'Process':<}{"Burst Time":<15}{"Waiting Time":<15}{"Turnaround Time"}")
    print("-" * 50)

    #defining the the tracking variables 

    #the frst process always waits 0 second so nothing runs before it 
    waiting_time = 0 
    #these are acumulators so you can calculate averages later
    total_waiting = 0 
    total_turnaround = 0
    
    for process in processes: #this goes through my list one at a time 
        Process_ID = process[0] #this grabs the process number
        burst_time = process[1] #this gets the burst time 

        turnaround = waiting_time + burst_time


        print(f"{Process_ID:<10}{burst_time:<15}{waiting_time:<15}{turnaround}")
        total_waiting += waiting_time
        total_turnaround += turnaround
        waiting_time += burst_time #the following process will wait for this one to finish


