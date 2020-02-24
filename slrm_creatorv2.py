def get_gjf(gjf_file):
    def slrm_opener(file):
        file_to_open = open(file, "r") 
        information = file_to_open.readlines()
        file_to_open.close() #it has to be closed
        return information
    
    def get_name(gjf_file):
        gjf_name = gjf_file.split(".")
        name = gjf_name[0]
        return name
    
    def rewrite_slrm_line(i):
        if i == 1: # #SBATCH -J {name}
            str = slrm.write(f"#SBATCH -J {name} \n")
        elif i == 2: # #SBATCH -o {name}.out
            str = slrm.write(f"#SBATCH -o {name}.out \n")
        elif i == 6: # #SBATCH -t 24:00:00
            str = slrm.write(f"#SBATCH -t {time} \n")
        elif i == 8: # #SBATCH --mail-user=kindlez98@gmail.com
            str = slrm.write(f"#SBATCH --mail-user={mail} \n")
        elif i == 27: # INPUT={name}.gjf
            str = slrm.write(f"INPUT={name}.gjf \n")
        elif i == 28: # OUTPUT={name} .out
            str = slrm.write(f"OUTPUT={name}.out \n")
        return str


    lines_for_change = [1,2,6,8,27,28]
    name = get_name(f'{gjf_file}')
    time = "24:00:00"
    mail = "kindlez98@gmail.com"
    information = slrm_opener("plantilla.slrm")
    i = 0
    slrm = open(f'{name}.slrm','w+')
    for linenum, line in enumerate(information):
                if i == len(lines_for_change):
                    slrm.write(line)
                else:
                    if linenum == lines_for_change[i]:
                        rewrite_slrm_line(linenum)
                        i += 1
                    else: 
                        slrm.write(line)
    slrm.close()
