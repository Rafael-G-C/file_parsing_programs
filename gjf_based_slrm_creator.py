import os.path as osp #library for os
import slrm_creatorv2 as sc #library for the creation of slrms


# add the gjf's files
list_of_files = []
while True:
    given_file = input("write the name of the input file, write 'cont' to continue\n") #let the user give the input file
    if given_file != "cont": # if the user writes "cont" it stops asking for files(we should make it so that it always puts in lowercase)
        if osp.isfile(f'{given_file}'): #check whether an input file exist https://docs.python.org/3/library/os.path.html#os.path.isfile
            list_of_files.append(given_file) #appends the files to the a list of files
        else:
            print(f'{given_file} does not exist')
    else: # breaks if the user writes "cont"
        break

#do the slrm
for i in range(len(list_of_files)): #will pass every file on the list_of_files to the slrm creator 
    sc.get_gjf(list_of_files[i])
print("the files have been created")



