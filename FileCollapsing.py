import os

def file_collapsing(WD, PATTERN):
    os.chdir(WD)
    lst = [file for file in os.listdir() if file.endswith(PATTERN)]
    header = None
    new_data = []
    first_file_processed=False

    for file_name in lst:
        with open(file_name, 'r') as file:
            lines = file.readlines()

            if not first_file_processed:
                header=lines.pop(0).strip()
                new_header=header+"\t"+"sample"
                first_file_processed=True
            else:
                lines.pop(0)
            new_data.extend(lines)

    for i in range(len(new_data)):
        new_data[i] = new_data[i].strip("\n") + "\t" + file_name + "\n"

    DEF=[]
    for row in new_data:
        DEF.append(row.strip("\t"))

    return new_header,"\n",DEF



# Reading files
cnv = file_collapsing("/Users/bxz262/Library/CloudStorage/GoogleDrive-bxz262@miami.edu/My Drive/Bachisio/Documents/PhD_PiBS_CAB/Courses/Courses_Spring2024/PIB_706_Informatics_for_the_Biosciences/Assignments/final_project_proposal/WORK/", ".facets.cnv.txt")

# Merging based on sample
cnv_1 = []
for row_cnv in cnv:
    cnv_1.append(row_cnv)

#print(cnv_1,type(cnv_1))

# Writing merged data to a new file
with open("merged_data.txt", "w") as merged_file:
    for row in cnv_1:
        #row=str(row)
        merged_file.write(''.join(row))
merged_file.close()
