import numpy as np


def STD_TXT(input_txt_dir, del_col_list):
    data = np.loadtxt(input_txt_dir)
    data = np.delete(data, del_col_list, axis=1)
    output_txt_dir = input_txt_dir.replace(input_txt_dir.split('\\')[-1], "new_" + input_txt_dir.split('/')[-1])
    np.savetxt(output_txt_dir, data, fmt='%.4f')

