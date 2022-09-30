import numpy as np
import math
from model import Model
from dmchunk import Chunk
import pandas as pd

def noise(s):
    rand = np.random.uniform(0.001,0.999)
    return s * math.log((1 - rand)/rand)

def time_to_pulses(time, t_0 = 0.011, a = 1.1, b = 0.015):
    pulses = 0
    pulse_duration = t_0
    while time >= pulse_duration:
        time = time - pulse_duration
        pulses += 1
        pulse_duration = a * pulse_duration + noise(b * a * pulse_duration)
    return pulses

def pulses_to_time(pulses, t_0 = 0.011, a = 1.1, b = 0.015):
    time = 0
    pulse_duration = t_0
    while pulses > 0:
        time = time + pulse_duration
        pulses = pulses - 1
        pulse_duration = a * pulse_duration + noise(b * a * pulse_duration)
    return time

def feedback(r, x):
     return ((r - x) / r) ** 2

def acerbi(n_participants):
    
#     n_participants = 10

    df = pd.DataFrame(columns = ["int", "resp", "probs" "feedback", "Subject", "Block", "Run", "Task", "Main"])

    short_intervals = np.linspace(450, 825, num = 6)
    medium_intervals = np.linspace(600, 975, num = 6)
    long_intervals = np.linspace(750, 1125, num = 6)

    prob = {"Short Uniform": [1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
            "Long Uniform": [1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
            "Medium Uniform": [1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
            "Medium spiked": [1/12, 7/12, 1/12, 1/12, 1/12, 1/12]}
    
    for subj in range(n_participants):
        
        if subj < 4:
            conditions = {"Short Uniform": short_intervals,
                          "Long Uniform": long_intervals}
            task = 1
        
        else:
            conditions = {"Medium Uniform": medium_intervals,
                          "Medium spiked": medium_intervals}
            task = 2
            
        for cond in conditions:
            m = Model()
            main = False
            
            #trial session
            train = np.random.randint(500, 1500)
            
            #2 test sessions
            test = train + 1000
            
            for trial in range(test):
                # print(trial)
                #initial 1s
                m.time += 1
                
                #random delay
                delay = np.random.uniform(0.25, 1)
                m.time += delay

                #interval
                interval = np.random.choice(conditions[cond], p = prob[cond])
                m.time += interval /1000
                pulses = time_to_pulses(interval / 1000)
                
                #Appearance of yellow dot
                m.time += 0.0185
                
                #Chunk is stored in DM
                chunk = Chunk(name = f"pulse{pulses}", slots = {"isa" : "time", "pulses": pulses})
                m.add_encounter(chunk)
                
                #wait of 250ms
                m.time += 0.25
                
                #reproduction of time interval
                pattern = Chunk(name = "retrieve", slots = {"isa": "time"})
                chunk, latency = m.retrieve(pattern)
                m.time += latency

                probs = m.get_retrieval_probability(chunk, pattern)
                
                time = pulses_to_time(chunk.slots["pulses"])
                m.time += time
                
                #delay of 450ms-850ms before feedback
                m.time += np.random.uniform(0.45, 0.85)
                
                #feedback
                fb = feedback(interval, time * 1000) * 1000
                
                #feedback display of 62ms
                m.time += 0.062
                
                #fixation cross
                m.time += np.random.uniform(0.5, 0.75)
                
                #black screen
                m.time += np.random.uniform(0.5, 0.75)
                
                #training sessions are recorded
                if trial > train:
                    main = True
                
                    df = df.append({"int": interval,
                                    "resp": time * 1000,
                                    "probs": probs,
                                    "feedback": fb,
                                    "Subject": subj + 1,
                                    "Block": cond,
                                    "Run": trial + 1,
                                    "Task": task,
                                    "Main": main}, ignore_index = True)
    return df

df = acerbi(1)