from os import dup
import os.path
import sys
import hashlib

def get_number_list(delete_list, maxnumber):
    newlist = []
    for fileno in delete_list:
        if not fileno.isnumeric():
            return []
        fileno = int(fileno)
        if 1 <= fileno <= maxnumber:
            newlist.append(fileno)
    return newlist

def get_delete_list(maxnumber):
    while True:
        print("Enter file numbers to delete:")
        line = input()
        print()
        if line != "":
            delete_list = line.split()
            delete_list = get_number_list(delete_list, maxnumber)
            if len(delete_list) > 0:
                return delete_list
        print("Wrong format")
        print()


def get_yesno():
    while True:
        yesno = input()
        if yesno in ("yes", "no"):
            return yesno
        print("Wrong option")

def get_hash(path):
    file = open(path, "rb")
    bytes = file.read()
    m = hashlib.md5(bytes)
    return m.digest()

def get_files(dir, file_format, files):
    for entry in os.listdir(dir):
        path = os.path.join(dir, entry)
        if os.path.isfile(path):
            filename, ext = os.path.splitext(path)
            if file_format == "" or ext.lower() == "." + file_format:
                files.append([path, os.path.getsize(path)])
        elif os.path.isdir(path):
            get_files(path, file_format, files)    

def delete_files(delete_list, dupfile_list):
    total_size = 0
    for fileno in delete_list:
        path, size = dupfile_list[fileno - 1]
        total_size += size
        os.remove(path)
    return total_size

# sys.argv.append(input())

if len(sys.argv) == 1:
    print("Directory is not specified")
    sys.exit()

print()
print("Enter file format:")
file_format = input().lower()
print()
print("Size sorting options:")
print("1. Descending")
print("2. Ascending")
print()
while True:
    print("Enter a sorting option:")
    sort_option = int(input())
    print()
    if sort_option in range(1, 3):
        break
    else:
        print("Wrong option")
    print()

files = []
get_files(sys.argv[1], file_format, files)
if sort_option == 1:
    files.sort(key=lambda x: x[1], reverse=True)
else:
    files.sort(key=lambda x: x[1])
   
sizedict = {}
for file in files:
    path, size = file
    if size in sizedict:
        pathlist = sizedict[size]
    else:
        pathlist = []
    pathlist.append(path)
    sizedict[size] = pathlist

for size in sizedict:
    pathlist = sizedict[size]
    if len(pathlist) < 2:
        continue
    print(size, "bytes")
    for path in pathlist:
        print(path)
    print()

while True:
    print("Check for duplicates?")
    yesno = input()
    print()
    if yesno in {"yes", "no"}:
        break

if yesno == "no":
    sys.exit()

sizehashdict = {}
for size in sizedict:
    pathlist = sizedict[size]
    if len(pathlist) < 2:
        continue
    hashdict = {}
    for path in pathlist:
        hash = get_hash(path)
        if hash in hashdict:
            value = hashdict[hash]
            value.append(path)
            hashdict[hash] = value
        else:
            hashdict[hash] = [path]
    sizehashdict[size] = hashdict

number = 0
dupfile_list = []
for size in sizehashdict:
    print(size, "bytes") 
    hashdict = sizehashdict[size]
    for hash in hashdict:
        pathlist = hashdict[hash]
        if len(pathlist) > 1:
            print(f"Hash: {hash.hex()}")
            for path in pathlist:
                number += 1
                dupfile_list.append([path, size])
                print(f"{number}. {path}")
    print()

print("Delete files?")
yesno = get_yesno()
if yesno == "no":
    sys.exit()

print()
delete_list = get_delete_list(number)

delete_size = delete_files(delete_list, dupfile_list)

print(f"Total freed up space: {delete_size} bytes")
