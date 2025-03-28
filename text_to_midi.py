from copy import deepcopy
import py_midicsv as pm
import os
import shutil

####################################################################
# Requires that the simplified_midi file finishes with a blank " " 
####################################################################

def create_midi_file(input_file_path,output_file_path, header):

    with open(input_file_path,"r") as file:
            simplified_midi = file.read()[:-1] 

    l = simplified_midi.split(' ')
    
    for i in range(len(l)):
        l[i] = l[i].split(':')
    
    for i in range(len(l)):

        for j in range(4):
            l[i][j] = int(l[i][j][1:])

    t_abs = 0
    for i in range (len(l)):
        l[i].append(t_abs)
        t_abs+= l[i][3]
    j=deepcopy(l)
    for a in j:
        l.append([a[0],0,0,0,a[4]+a[2]])
    l = sorted(l, key=lambda x: x[4])
    l.append([0,0,0,0,l[-1][4]])

    csv_string = deepcopy(header)

    for i in range(len(l)):

        csv_string.append("2, " + str(l[i][4]) + ", Note_on_c, 0, " + str(l[i][0]) + ", " + str(l[i][1]) + "\n")

    csv_string.append("2, " + str(l[len(l)-1][4]) + ", End_track\n")

    csv_string.append("0, 0, End_of_file")

    midi_object = pm.csv_to_midi(csv_string)

    with open(output_file_path, "wb") as output_file :
        midi_writer = pm.FileWriter(output_file)
        midi_writer.write(midi_object)


