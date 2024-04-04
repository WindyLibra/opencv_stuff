from pathlib import Path
import os
import shutil

folder_name = "David_rszo_30_08_23_14_03"

#В new_dir пишем название новой папки
new_dir = f'{folder_name}_labeled' #

# В home записываем путь к пользователю
home = Path.home()

# В absolute записываем путь к папке с фотографиями
#absolute = "C:/Users/aram_/OneDrive/Documents/Videos_and_Images_for_Test/For Machine Learning/ML 1st batch/David_bmp_car_09_08_23_11_29"

absolute = Path(home, "OneDrive", "Documents", "Videos_and_Images_for_Test", "For Machine Learning", "Toy MRLS", folder_name)

# В new_absolute записываем путь к папке до папки с фотографиями, для того чтобы в этом месте создать результирующую папку
new_absolute = absolute.parent

# В path записываем объединение путя к папке с названием новой результирующей папки
path = os.path.join(new_absolute, new_dir)
os.mkdir(path)


names = []
picture = ''
check_picture = ''

#В цикле проходим по каждому файлу папки, если встречается xml файл то создаём его копию в новой папке при помощи shutil.copy2, получаем только название файла при промощи stem и записываем названия в список
for all_elem in absolute.glob('*.*'):
    if Path(all_elem).suffix == '.xml':
        copy_file = shutil.copy2(all_elem, path)
        picture = Path(all_elem).stem
        names.append(picture)

#В цикле проходим по каждому jpg файлу папки, получаем только название файла при промощи stem и сравниваем это название с названиями из списка, если нашлось похожее название то создаём его копию в новой папке при помощи shutil.copy2
for all_elem in absolute.glob('*.jpg'):
    check_picture = Path(all_elem).stem
    for elem in names:
        if check_picture == elem:
            copy_file = shutil.copy2(all_elem, path)