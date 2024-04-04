# Переименование файлов если вдруг забыл сделать

import os

# не забывайте менять это перед запуском
# не забывайте так же поменять имя папки
rename_name = 'David_rszo_30_08_23_14_03'
folder = f'C:/Users/aram_/OneDrive/Documents/Videos_and_Images_for_Test/For Machine Learning/Toy MRLS/{rename_name}'  # <---------- вот тут
to_be_replaced = 'Davod_rszo_30_08_23_14_03'

counter = 0

for count, filename in enumerate(os.listdir(folder)):
    dst = filename.replace(to_be_replaced, rename_name)
    src = f"{folder}/{filename}"  # folder-name/filename, if .py file is outside folder
    dst = f"{folder}/{dst}"

    os.rename(src, dst)
    counter += 1

print(counter)



