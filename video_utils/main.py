import xml.etree.ElementTree as ET
from glob import glob
import os
from natsort import natsorted


def main():
    """
    p_* -> paths
    l_* -> list
    is_* -> boolean
    :return:
    Shift - object not from first frame - frame number
    Video name - >

    review shift
    review file count
    review label sorting(?)
    all labels should start from 0
    """

    p_absolute = 'C:\\Users\\aram_\\PycharmProjects\\PrepareDataForTracking'
    p_txt_files = p_absolute + "\\txt_files\\"
    if not os.path.exists(p_txt_files):
        os.mkdir(p_txt_files)
    l_folders = glob(f"{p_absolute}/*/", recursive=True)
    for folder in l_folders:
        l_objects_dirs = natsorted(glob(f"{folder}/*/", recursive=True)) # sorted -> natsorted
        counter = 0
        root_dir = folder.split('\\')[-2]
        if os.path.exists(p_txt_files + root_dir + '.txt'):
            continue
        is_first_object = True
        if folder not in p_txt_files:
            for p_objects in l_objects_dirs:
                is_first_frame = True
                l_annotations = sorted(glob(f'{p_objects}*.xml'))
                if is_first_object:
                    new_file_name = f'{p_txt_files}{root_dir}.txt'  # f'{p_txt_files}{root_dir}.txt'
                else:
                    new_file_name = f'{p_txt_files}{root_dir}_{counter - 1}.txt'  # f'{p_txt_files}{root_dir}_{counter - 1}.txt'
                counter += 1
                with open(new_file_name, 'w') as f:
                    if is_first_object:
                        # -1, since /txt_file/ dir is there too
                        f.write(f"files: {len(l_objects_dirs)}\n") # - 1
                        is_first_object = False

                    print(f"{new_file_name.split('//')[-1]} is created!")
                    l_sorted_annotations = natsorted(l_annotations)
                    for file in l_sorted_annotations:
                        # print('file=', file)

                        parsedXML = ET.parse(file)
                        if parsedXML:
                            for node in parsedXML.getroot().iter('object'):
                                blood_cells = node.find('name').text
                                if "warning" in blood_cells:
                                    print(blood_cells.split('_'), file.split('\\')[-2], file.split('\\')[-1])
                                    is_warning = True
                                else:
                                    is_warning = False
                                xmin = node.find('bndbox/xmin').text
                                ymin = node.find('bndbox/ymin').text
                                xmax = node.find('bndbox/xmax').text
                                ymax = node.find('bndbox/ymax').text
                                string = f"{xmin} {ymin} {xmax} {ymax}\n"
                                try:
                                    frame_number = int(os.path.splitext(file)[0].split('_')[-1])
                                except:
                                    print("Something wrong in file name, it must be videoname_framenumber.xml")
                                    print(file)
                                    exit(2)
                                if is_first_frame:
                                    f.write(f"shift: {frame_number - 1}\n") # - 1
                                    x_center = round((int(xmin) + int(xmax)) / 2)
                                    y_center = round((int(ymin) + int(ymax)) / 2)
                                    f.write(f"coordinates: {x_center} {y_center}\n")
                                    is_first_frame = False
                                if is_warning:
                                    string = f"{frame_number - 1} {xmin} {ymin} {xmax} {ymax}\n"
                                f.write(string)
                        else:
                            print(f"Can't parse {file}")
                    f.close()


if __name__ == "__main__":
    main()
