import copy as cp
import pandas as pd
import os.path as osp
def file_opener(file):
        file_to_open = open(file, "r") 
        information = file_to_open.readlines()
        file_to_open.close() #it has to be closed
        file_split = file.split(".")
        name = file_split[0]
        return information, name

def minimum_energies(information):
    linenum_energy_pair = {}
    for linenum, line in enumerate(information):
        if "SCF Done:" in line:
            scf_line = linenum
            energy_extract = line.split()
            local_minimum_energy = float(energy_extract[4])
            linenum_energy_pair[local_minimum_energy] = scf_line
    global_minimum_energy = min(linenum_energy_pair)
    #print(global_minimum_energy)
    global_minimum_energy_line = linenum_energy_pair[global_minimum_energy]
    
    return global_minimum_energy,global_minimum_energy_line,linenum_energy_pair

def geometry_lookup(information):
    standard_orientation_line = []

    for linenum, line in enumerate(information):
        if "Standard orientation:" in line:
            standard_orientation_line.append(linenum)
    
    return standard_orientation_line

def minimum_geometry(info):
    delta_line_line_pair = {}
    minimum_energy_line = minimum_energies(info)
    standard_orientation_lines = geometry_lookup(info)
    for line in standard_orientation_lines:
        if line < minimum_energy_line:
            delta_line = line - minimum_energy_line
            delta_line_line_pair[delta_line] = line
        max_line = max(delta_line_line_pair)
    return delta_line_line_pair[max_line]

def minimum_geometry_extract(information,geometry_line):
    column_names = ["Atom number","X","Y","Z"]
    minimum_coordinates = []
    dictionary_for_sorting = {}
    for linenum, line in enumerate(information):
        if linenum > geometry_line + 4 and "--" in line:
            break
        elif linenum > geometry_line + 4:
            splitted_line = line.split()
            atom_number = splitted_line[0]
            minimum_coordinates.append(splitted_line[1])
            for coordinate in range(3,6):
                minimum_coordinates.append((splitted_line[coordinate]))
            minimum_coordinates_copy = cp.deepcopy(minimum_coordinates)
            dictionary_for_sorting[atom_number] = minimum_coordinates_copy
            minimum_coordinates.clear()
    
    data_frame = pd.DataFrame.from_dict(dictionary_for_sorting,orient='index',columns=column_names)
    sorted_data_frame = data_frame.sort_values(by="Atom number",ascending=False)
    return sorted_data_frame
        
if __name__ == "__main__":
    path = "/home/kilimanjaro/Documents/computacional/"
    files = ["N151.out"]
    for file in files:
        info, name = file_opener(osp.join(path,file))
        min_geom_line = minimum_geometry(info)
        sorted_geometry = minimum_geometry_extract(info,min_geom_line)
        sorted_geometry.to_csv(osp.join(path,name+".csv"),index=False)
        print(file)
        print(min_geom_line)
        print()
        