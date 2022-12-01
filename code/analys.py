# =============================================================================
# Mini Project 2: Rush Hours.
# Analysis code.
# =============================================================================

from os import listdir
from os.path import isfile, join
import pandas as pd

A_star_folder= "/home/damien/Desktop/SCHOOL/Concordia/COMP_472/Mini_projects/MP2/A_tests"
gbfs_folder = "/home/damien/Desktop/SCHOOL/Concordia/COMP_472/Mini_projects/MP2/gbfs_tests"
ucs_folder = "/home/damien/Desktop/SCHOOL/Concordia/COMP_472/Mini_projects/MP2/ucs_tests"
fichiers_star = [f for f in listdir(A_star_folder) if isfile(join(A_star_folder, f))]
fichiers_gbfs = [f for f in listdir(gbfs_folder) if isfile(join(gbfs_folder, f))]
fichiers_ucs = [f for f in listdir(ucs_folder) if isfile(join(ucs_folder, f))]
files_all = [fichiers_star,fichiers_gbfs,fichiers_ucs]
content_star = list()
content_gbfs = list()
content_ucs = list()
buffer = list()
for files in files_all:
    for file in files:
        if files == files_all[0]:
            f = open("/home/damien/Desktop/SCHOOL/Concordia/COMP_472/Mini_projects/MP2/A_tests/" + file, 'r')
        elif files == files_all[1]:
            f = open("/home/damien/Desktop/SCHOOL/Concordia/COMP_472/Mini_projects/MP2/gbfs_tests/" + file, 'r')
        else:
            f = open("/home/damien/Desktop/SCHOOL/Concordia/COMP_472/Mini_projects/MP2/ucs_tests/" + file, 'r')
        try:
            content = f.readlines()[10:13]
            if content[0][0] == 'R':
                if files == files_all[0]:
                    buffer.append(file.split('-')[3].split('.')[0])
                    buffer.append('A*')
                    buffer.append(file.split('-')[2])
                if files == files_all[1]:
                    buffer.append(file.split('-')[3].split('.')[0])
                    buffer.append('gbfs')
                    buffer.append(file.split('-')[2])
                if files == files_all[2]:
                    buffer.append(file.split('-')[2].split('.')[0])
                    buffer.append('ucs')
                    buffer.append('NA')
                buffer.append(float(content[1].split(' ')[3]))
                buffer.append(float(content[2].split(' ')[3]))
                buffer.append(float(content[0].split(' ')[1]))

        except:
            continue
        if buffer != []:
            if files == files_all[0]:
                content_star.append(buffer)
            elif files == files_all[1]:
                content_gbfs.append(buffer)
            else:
                content_ucs.append(buffer)
        buffer = []

cont = []
for i in range(len(content_star)):
    cont.append(content_star[i])
    cont.append(content_gbfs[i])
    try:
        cont.append(content_ucs[i])
    except:
        continue

data = pd.DataFrame(cont, columns=["puzzle number", "algorithm", "heuristic", "length of the search path","length of the solution", "Execution time (seconds)"])
data.to_csv('result.csv')
info = list()
for algo in ['ucs', 'gbfs', 'A*']:
    buf = list()
    if algo == 'ucs':
        for value in ["length of the search path","length of the solution", "Execution time (seconds)"]:
            v = data.loc[data['algorithm'] == 'ucs', value].sum() / len(data.loc[data['algorithm'] == 'ucs', value])
            buf.append(round(v, 4))
    else:
        for h in ['h1', 'h2', 'h3', 'h4', 'h5']:
            for value in ["length of the search path","length of the solution", "Execution time (seconds)"]:
                v = data.loc[(data['algorithm'] == algo)  & (data['heuristic'] == h), value].sum()  / \
                    len(data.loc[(data['algorithm'] == algo)  & (data['heuristic'] == h), value])
                buf.append(round(v, 4))
    info.append(buf)

columns = ['length of the search path (for gbfs and A* heuristic = 1)','length of the solution (for gbfs and A* heuristic = 1)',
           'Execution time (seconds) (for gbfs and A* heuristic = 1)', 'length of the search path (for gbfs and A* heuristic = 2)','length of the solution (for gbfs and A* heuristic = 2)',
           'Execution time (seconds) (for gbfs and A* heuristic = 2)', 'length of the search path (for gbfs and A* heuristic = 3)','length of the solution (for gbfs and A* heuristic = 3)',
           'Execution time (seconds) (for gbfs and A* heuristic = 3)', 'length of the search path (for gbfs and A* heuristic = 4)','length of the solution (for gbfs and A* heuristic = 4)',
           'Execution time (seconds) (for gbfs and A* heuristic = 4)', 'length of the search path (for gbfs and A* heuristic = 5)','length of the solution (for gbfs and A* heuristic = 5)',
           'Execution time (seconds) (for gbfs and A* heuristic = 5)']
data_mean  =pd.DataFrame(info, index=['ucs', 'gbfs','A*'], columns=columns)
data_mean.to_csv('analys.csv')
