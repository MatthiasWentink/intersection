import math
from sympy import *
from midiutil import MIDIFile
import numpy as np

from track import Track
from interval import Interval

def get_velocity(x:Expr,y:Expr,intersection_t:float) -> float:
    x = diff(x,Symbol('theta')).subs({'theta':intersection_t})
    y = diff(y,Symbol('theta')).subs({'theta':intersection_t})
    return math.sqrt(x**2+y**2)

def get_velocities(x:Expr,y:Expr,intersections:list[float]) -> list[float]:
    return [get_velocity(x,y,intersection) for intersection in intersections]

def normalize_velocities(x:list[float]) -> list[float]:
    softmax = np.exp(x) / np.sum(np.exp(x), axis=0)
    return [int(50+50*velocity) for velocity in softmax]

def get_intersection(x: Expr,y: Expr, pitch:int, t_range=Interval(-20*pi,20*pi)) -> Track:
    original = solve(x)
    result = []
    for root in original:
        i = 0
        period = get_period(original)
        current_t = root
        print(t_range)
        while(t_range.in_range(current_t)):
            if not current_t in result:
                result.append(current_t)
            i = i + 1
            current_t = root + i * abs(period)
    result = sorted(result)
    return Track(result, get_velocities(x,y, result), pitch)
   
def get_period(numbers:list[float]) -> float:
    eligible = numbers.copy()
    if 0 in eligible:
        eligible.remove(0)
    return min([number for number in eligible if number.is_real])

def intersections_to_midi(bpm:int, file_name="rhythm", *tracks:list[Track]):
    midi = MIDIFile(1)
    midi.addTempo(track=0, time=0, tempo=bpm)

    beats = bpm / 60 * 4
    times = [time for track in tracks for time in track.times]
    start, end = min(times), max(times)
    for track in tracks:
        track_times = intersections_to_time(track.times,start,end, beats)
        track_volumes = normalize_velocities(track.volume)
        for i in range(len(track_times)):
            midi.addNote(track=0, channel=0, time=track_times[i], pitch=track.pitch, duration=0.5, volume=track_volumes[i])   
    
    with open("output/" + file_name + ".mid", "wb") as f:
        midi.writeFile(f)

def intersections_to_time(times:list[float], start:float, end:float, beats:int) -> list[float]:
    return [beats * ((time-start) / (end-start)) for time in times ]

   
def intersection_with_function(x:Expr,y:Expr,fun:Expr, pitch:int, t_range=Interval(-2*pi,2*pi)) -> Track:   
    substitution = fun.subs({'x':x}) - y
    intersections = solve(substitution)
    solutions = [intersection for intersection in intersections if t_range.in_range(intersection)]
    result = []
    for solution in solutions:
        i = 0
        period = get_period(solutions)
        current_t = solution
        while(t_range.in_range(current_t)):
            if not current_t in result and substitution.subs({'theta':current_t}).is_zero:
                result.append(current_t)
            i = i + 1
            current_t = solution + i * abs(period)
    result = sorted(result)
    return Track(result, get_velocities(x,y,result), pitch)