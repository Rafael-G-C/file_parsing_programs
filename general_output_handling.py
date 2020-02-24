def output_handle(file):

    def file_opener(file):
        file_to_open = open(file, "r") 
        information = file_to_open.readlines()
        file_to_open.close() #it has to be closed
        return information

    def number_of_calculations(information):
        calculations = []
        noc_counter = 0 #noc = number_of_calculations
        for line in information:
            if "#" in line and r"\#" not in line:
                calculations.append(line)
                noc_counter += 1
        noc_counter 
        return noc_counter, calculations

    def normal_termination(information):
        nt_counter = 0 #nt = normal_termination
        for line in information:
            if "Normal termination of Gaussian" in line:
                nt_counter += 1
        return nt_counter

    def main(file):
        info = file_opener(file)
        norc, calculations = number_of_calculations(info)
        nt = normal_termination(info)
        if norc == nt:
            print(f'{file} finished correctly')
        else:
            print(f"{file} failed {calculations[-1]}")


    main(file)
if __name__ == "__main__":
    files = ["N5.out"]
    for file in range(len(files)):
        output_handle(files[file])    


