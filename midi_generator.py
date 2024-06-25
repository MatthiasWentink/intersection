import math
from sympy import *
from midiutil import MIDIFile
import numpy as np

def get_velocity(x,y,intersection_t):
    x = diff(x,Symbol('theta')).subs({'theta':intersection_t})
    y = diff(y,Symbol('theta')).subs({'theta':intersection_t})
    return math.sqrt(x**2+y**2)

def get_velocities(x,y,intersections):
    return [get_velocity(x,y,intersection) for intersection in intersections]

def normalize_velocities(x):
    softmax = np.exp(x) / np.sum(np.exp(x), axis=0)
    return [int(50+50*velocity) for velocity in softmax]

def get_intersection(x,y, pitch, t_range=[-20*pi,20*pi]):
    # Return intersectionion with axis as well as velocity on those points
    original = solve(x)
    result = []
    for root in original:
        i = 0
        period = get_period(original)
        current_t = root
        while(in_range(current_t,t_range)):
            if not current_t in result:
                result.append(current_t)
            i = i + 1
            current_t = root + i * abs(period)
    result = sorted(result)
    return result, get_velocities(x,y, result), pitch
   
def in_range(number: int,range: list):
    return N(number) >= range[0] and N(number) <= range[1] and number.is_real

def is_root(x,t,current_t):
    return x.subs({'theta': current_t}) == 0

def get_period(numbers):
    eligible = numbers.copy()
    if 0 in eligible:
        eligible.remove(0)
    return min([number for number in eligible if number.is_real])

def intersections_to_midi(bpm, file_name="rhythm", *tracks):
    midi = MIDIFile(1)
    midi.addTempo(track=0, time=0, tempo=bpm)

    beats = bpm / 60 * 4
    times = [time for track in tracks for time in track[0]]
    start, end = min(times), max(times)
    for track in tracks:
        track_times = intersections_to_time(track[0],start,end, beats)
        track_volumes = normalize_velocities(track[1])
        for i in range(len(track_times)):
            midi.addNote(track=0, channel=0, time=track_times[i], pitch=track[2], duration=0.5, volume=track_volumes[i])   
    
    with open("output/" + file_name + ".mid", "wb") as f:
        midi.writeFile(f)

def intersections_to_time(track, start, end, beats):
    return [beats * ((time-start) / (end-start)) for time in track ]

   
def intersection_with_function(x,y,fun, pitch, t_range=[-2*pi,2*pi]):   
    substitution = fun.subs({'x':x}) - y
    intersections = solve(substitution)
    solutions = [intersection for intersection in intersections if N(intersection) >= t_range[0] and N(intersection) <= t_range[1]]
    print(solutions)
    result = []
    for solution in solutions:
        i = 0
        period = get_period(solutions)
        current_t = solution
        while(in_range(current_t,t_range)):
            if not current_t in result and substitution.subs({'theta':current_t}).is_zero:
                result.append(current_t)
            i = i + 1
            current_t = solution + i * abs(period)
    print(result)
    result = sorted(result)

    return result, get_velocities(x,y,result), pitch