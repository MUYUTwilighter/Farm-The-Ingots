from os import listdir

dir1 = "C:\\Games\\Minecraft\\.minecraft\\versions\\Farm The Ingots\\mods"
dir2 = "C:\\Games\\Minecraft\\.minecraft\\versions\\Farm The Ingots-test\\mods"

file1 = listdir(dir1)
file2 = listdir(dir2)

print("dir1 √ dir2 ×")
for i in file1:
    if i not in file2:
        print(i)

print("\ndir1 × dir2 √")
for i in file2:
    if i not in file1:
        print(i)