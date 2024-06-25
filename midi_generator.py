import math
from sympy import *
from midiutil import MIDIFile
import numpy as np

from track import Track
from interval import Interval
from volume import Volume

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
    times = []
    for root in original:
        i = 0
        period = get_period(original)
        current_time = root
        while(t_range.in_range(current_time)):
            if not current_time in times:
                times.append(current_time)
            i = i + 1
            current_time = root + i * abs(period)
    times = sorted(times)
    panning = get_panning(x,times)
    return Track(times, get_velocities(x,y, times), get_panning(x,times), pitch)

def get_panning(x: Expr, intersections: float) -> list[float]:
    return [N(x.subs({'theta':intersection})) for intersection in intersections]

   
def get_period(numbers:list[float]) -> float:
    eligible = numbers.copy()
    if 0 in eligible:
        eligible.remove(0)
    return min([number for number in eligible if number.is_real])

def intersections_to_midi(bpm:int, file_name="rhythm", *tracks:list[Track]):
    midi = MIDIFile(2)
    midi.addTempo(track=0, time=0, tempo=bpm)
    midi.addTempo(track=1, time=0, tempo=bpm)

    beats = bpm / 60 * 4
    times = [time for track in tracks for time in track.times]
    start, end = min(times), max(times)
    for track in tracks:
        track_times = intersections_to_time(track.times,start,end, beats)
        track_volumes = normalize_velocities(track.volume)
        max_pan = max([abs(pan) for pan in track.panning])
        normalized_panning = [pan/max_pan if max_pan != 0 else 0 for pan in track.panning]
        add_notes(midi,track_times,track_volumes,normalized_panning,track.pitch)
    
    with open("output/" + file_name + ".mid", "wb") as f:
        midi.writeFile(f)

def add_notes(midi,times,volumes,panning,pitch):
    for i in range(len(times)):
        volume = Volume(volumes[i],panning[i])
        midi.addNote(track=0, channel=0, time=times[i], pitch=pitch, duration=0.5,volume=volume.left)
        midi.addNote(track=1, channel=0, time=times[i], pitch=pitch, duration=0.5,volume=volume.right)      


def intersections_to_time(times:list[float], start:float, end:float, beats:int) -> list[float]:
    return [beats * ((time-start) / (end-start)) for time in times ]

   
def intersection_with_function(x:Expr,y:Expr,fun:Expr, pitch:int, t_range=Interval(-2*pi,2*pi)) -> Track:   
    substitution = fun.subs({'x':x}) - y
    intersections = solve(substitution)
    solutions = [intersection for intersection in intersections if t_range.in_range(intersection)]
    times = []
    for solution in solutions:
        i = 0
        period = get_period(solutions)
        current_time = solution
        while(t_range.in_range(current_time)):
            if not current_time in times and substitution.subs({'theta':current_time}).is_zero:
                times.append(current_time)
            i = i + 1
            current_time = solution + i * abs(period)
    times = sorted(times)
    return Track(times, get_velocities(x,y,times), get_panning(x,times), pitch)
