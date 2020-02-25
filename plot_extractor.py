# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#%matplotlib notebook #this magic method lets us work with the graph
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import general_output_handling as goh


# %%
#read file
def file_opener(file): #open the IR file for reading
    file_to_open = open(file, "r") 
    information = file_to_open.readlines()
    file_to_open.close() #it has to be closed
    name_extract = file.split(".")
    name = name_extract[0]
    return information, name


def info_extract(information,choice):
    if choice == 0: #UV_vis extract
        wavelength = []
        force = [] 
        #stop_counter = 0
        for line in information: #"linenum" tells us which line we are on in the for loop (in order to work we need "enumerate"). "line" is the actual line been read at the momment
            if "Excited State" in line: #search for the word "Excited State" in the file
                excited_state_split = line.split() #split the line
                force_extract = excited_state_split[8] # extract the part that contains the force (f=XXX in the file)
                force.append(float(force_extract[2:8])) #"[2:8]" extracts the number and "float" makes the number a float value
                wavelength.append(float(excited_state_split[6])) #extract the wavelength (nm) from the splitted line
                #stop_counter = 1
            #elif "->" in line:
                #stop_counter = 0
            #else:
                #stop_counter += 1

            #if stop_counter == 6:
                #break
        #print(wavelength)
        #print(force)
        extracted_x = wavelength
        extracted_y = force
        neg_freq = 0
    
    elif choice == 1: #IR extract

        freq = []
        freq_int = []
        for line in information:
            if "Frequencies --" in line: #look for the word "Frequencies --" in the line (this is how gaussian reads them)
                freq_split = line.split() #if it is split it 
                for i in range(2,5): #we want the 2 to  5 values from the array
                    freq.append(float(freq_split[i])) #append the values to the frequencies list
            elif "IR Inten    --" in line: #look for the intensities in the line
                freq_int_split = line.split() #split it
                for i in range(3,6): #we only care for the values 3 to 6
                    freq_int.append(-1*(float(freq_int_split[i]))) #the values go below zero so substracting hence why I substract 1000 (which is arbitrary)
        #print(freq)
        #print(freq_int)
        extracted_x = freq
        extracted_y = freq_int
        neg_freq = neg_freq_check(extracted_x)
        
    return neg_freq,extracted_x, extracted_y
    
def neg_freq_check(extracted_x):
    neg_freq = 0
    for x in extracted_x:
        if x < 0:
            neg_freq += 1
    return neg_freq
            
            
def x_sweep(starting_x,ending_x,space_between_numbers):
    delta_x = ending_x-starting_x+1
    number_divisions = delta_x/space_between_numbers
    x_values = np.linspace(starting_x,ending_x,round(number_divisions))
    return x_values

def y_function(x_extracted,y_extracted,x_sweep,signal_width,starting_x,ending_x,choice):
    new_x = []
    new_y = []
    for value in range(len(x_extracted)):
        if x_extracted[value] > starting_x and x_extracted[value] < ending_x:
            new_x.append(x_extracted[value])
            new_y.append(y_extracted[value])
    
    y_values = np.zeros(len(x_sweep))

    
    for y_value in range(len(new_y)):
        y_value_index = 0
        for x_value in range(len(x_sweep)):
            if choice == 0: #gaussian
                y_values[y_value_index] = new_y[y_value]*np.exp(-1*(np.log(2)*((x_sweep[x_value] - new_x[y_value])/signal_width)**2)) + y_values[y_value_index]
            elif choice == 1: #lorentzian
                y_values[y_value_index] = new_y[y_value]/(1+((x_sweep[x_value] - new_x[y_value])/signal_width)**2) + y_values[y_value_index]
            #print(f'x {x_sweep[x_value]} y {y_values[y_value_index]}')
            y_value_index += 1
        
    #print(uvvis_inten)
    return y_values 

def merge_names(list_of_names):
    total_name = list_of_names[0]
    for names in range(len(list_of_names)-1):
        total_name = total_name+"_"+list_of_names[names+1]
    return total_name
def merge_y(y_values):
    np_array_y = np.array(y_values)
    sum_of_y = []
    for y in range(len(np_array_y[0])):
        summed_y = np.sum(np_array_y[:,y])
        sum_of_y.append(summed_y)
    return sum_of_y


# %%
#parameters
merge_y_n = 0
IR_or_UV = 0 #uv_vis = 0 IR = 1 
G_or_L = 0 #gaussian = 0 lorentzian = 1
signal_width = 3
space_between_numbers = 0.3
starting_x = 190
ending_x = 800
#because we in this case we want to compare the tautomeric forms of a molecule we extract the info from bothh outputs and then just plor the information
files = ["N117.out","N119.out","N120.out","N121.out","N122.out","N123.out","N53.out","N54.out","N55.out","N56.out","N59.out","N60.out"]
file_names = []
total_name = "default"
max_x_per_file = []
max_y_per_file = []
x_values = []
y_values = []
for file in range(len(files)):
    goh.output_handle(files[file])
    info, name = file_opener(files[file])
    file_names.append(name)
    
    neg_freq,max_x, max_y = info_extract(info,IR_or_UV)
    max_x_per_file.append(max_x)
    max_y_per_file.append(max_y)
    
    if len(x_values) == 0:
        x_values.append(x_sweep(starting_x,ending_x,space_between_numbers))
    
    y_values.append(y_function(max_x_per_file[file],max_y_per_file[file],x_values[0],signal_width,starting_x,ending_x,G_or_L))
    
    if neg_freq != 0:
        print(f'file {name} has {neg_freq}  negative frequencies')


if len(files) != 1:
    total_name = merge_names(file_names)
    
if merge_y_n == 1:    
    y_values.append(merge_y(y_values))
    file_names.append(total_name)
    total_name = total_name+"M"

py_y_values = np.array(y_values)

data_columns = py_y_values.transpose()
df = pd.DataFrame(data=data_columns,index=x_values,columns=file_names)
df.to_csv(total_name+".csv",encoding='utf-8',)

df
df.plot()






