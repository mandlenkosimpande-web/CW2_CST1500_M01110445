import streamlit as st
import threading
import pandas as pd
import plotly.express as px 

st.set_page_config(page_title="FCFS CPU Scheduling", page_icon="🖥️", layout="wide")
st.title("💣 First Come First Served - CPU Scheduling")

#first come first served is a CPU scheduling algorithm. processes are executed in the order they arrive with no preemption.
def fcfs(processes):
    #defining the tracking variables

    #the first process always waits 0 seconds so nothing runs before it
    waiting_time = 0
    #these are accumulators so you can calculate averages later
    total_waiting = 0
    total_turnaround = 0

    results = [] #storing results so we can display them in the table

    for process in processes: #this goes through my list one at a time
        Process_ID = process[0] #this grabs the process number
        burst_time = process[1] #this gets the burst time

        turnaround = waiting_time + burst_time

        results.append({
            'Process ID': Process_ID,
            'Burst Time': burst_time,
            'Waiting Time': waiting_time,
            'Turnaround Time': turnaround
        })

        total_waiting += waiting_time
        total_turnaround += turnaround
        waiting_time += burst_time #the following process will wait for this one to finish

    np = len(processes)
    avg_waiting = total_waiting / np
    avg_turnaround = total_turnaround / np

    return results, avg_waiting, avg_turnaround

st.subheader("Enter Process Details")

np = st.number_input(
    "How many processes?",
    min_value=1,
    step=1,
    value=1
) # it asks the user how many processes they would like to enter

processes = []
for i in range(int(np)):
    burst_time = st.number_input( #st.number input is a streamlit function that creates a number input field. it takes in a label, a minimum value, a step value, and a key. the key is used to identify the input field so that the value can be retrieved later. the label is what is displayed to the user. the minimum value is the lowest value that can be entered. the step value is how much the value will increase or decrease when the user clicks the up or down arrow.
        f"Enter Burst Time for process {i+1}: ",
        min_value=0,
        step=1,
        key=f"burst_{i}"
    )
    processes.append((i+1, burst_time))


if st.button("Run FCFS"):
    #creating a thread so that fcfs is run inside it. though unnecessary I've added it as a show of skill and knowledge and will run efficiently without it.
    result_holder = {}

    def run_fcfs():
        results, avg_waiting, avg_turnaround = fcfs(processes)
        result_holder['results'] = results
        result_holder['avg_waiting'] = avg_waiting
        result_holder['avg_turnaround'] = avg_turnaround
#creating a thread so that fcfs is run inside it. though unecesary I've added it as a show of skill and knkowledge and will run effeciently without it.
    thread = threading.Thread(target=run_fcfs)
    thread.start()
    thread.join()

    
    st.subheader("Results")
    st.table(result_holder['results'])

    col1, col2 = st.columns(2)
    col1.metric("Average Waiting Time", f"{result_holder['avg_waiting']:.2f}")
    col2.metric("Average Turnaround Time", f"{result_holder['avg_turnaround']:.2f}") #:.2f is what im using to format the number to 2 decimal places. 

   
    gantt_data = [] # this is a list to store the data for the Gantt chart
    start_time = 0 # this is the time when the next process will start, setting it to 0 so that the first process starts at time 0

    for row in result_holder['results']:
        gantt_data.append({ #im appending a dictionary to the gantt_data list for each prosess. itll allow me to creat a gantt chart later with the information in the list 
            'Process': f"P{row['Process ID']}",
            'Start': start_time,
            'Finish': start_time + row['Burst Time'],
            'Burst Time': row['Burst Time']
        })
        start_time += row['Burst Time'] #the next process starts where this one ends

    df_gantt = pd.DataFrame(gantt_data) # here I am creating a dataframe from the gantt_data list so that I can use it to create a Gantt chart using plotly express. I am using a dataframe because it is easier to work with and manipulate data in a dataframe than in a list of dictionaries.

    #using a bar chart so that the use can visualize the processes and their burst times in a Gantt chart format
    fig = px.bar(
        df_gantt,
        base='Start', #this is the starting point of the bar
        x='Burst Time', #this is the width of the bar
        y='Process', #this is the y axis which is the process ID
        color='Process', #this is the color of the bar
        orientation='h', #this is the orientation of the bar
        title='FCFS Gantt Chart', #
        labels={'Burst Time': 'Time Units', 'Process': 'Process ID'}
    )#in this part i was basicaly creating the format of the Gantt chart and how it would look. I used a bar chart because it is the most similar to a Gantt chart and is easy to understand for the user.

    #in this part of my code i am reversing the y axis so that the first process is at the top and the last process is at the bottom. this is because in a Gantt chart the first process is at the top and the last process is at the bottom.
    fig.update_yaxes(autorange=True)
    fig.update_layout(xaxis_title="Time Units", yaxis_title="Process")

    st.subheader("Gantt Chart")
    st.plotly_chart(fig, use_container_width=True)