from zdspy import rom_util
from zdspy import map2d
from zdspy import dataio as d
import os
import randomize
import random

print("###############################")
print("")
print("1 - Randomize Entrances")
print("2 - Extract ROM")
print("3 - Re-Insert Files into ROM")
print("4 - Dump Map2D from ROM")
print("")
print("###############################")


choice = input("> ")
if choice == "4":
    print("### Map2D dumper ###")
    indir = "./extracted/root/Map2D"
    if not os.path.exists(indir):
        print("Drag and Drop your ROM in here or provide the path.")
        rom_path = input("> ")
        rom_util.extract(rom_path, "./extracted/root/", confirm=True)
    map2d.dump_bitmap_all(indir, "./infodump/Map2D/")
elif choice == "2":
    print("### EXTRACT ROM CONTENTS ###")
    print("Drag and Drop your ROM in here or provide the path.")
    rom_path = input("> ")
    rom_util.extract(rom_path, "./extracted/root/", confirm=True)
elif choice == "3":
    print("### REINSERT ROM CONTENTS ###")
    print("Drag and Drop your ROM in here or provide the path.")
    rom_path = input("> ")
    print("Drag and Drop the replacement root folder in here or provide the path.")
    replacement_data_root = os.path.abspath(input("> ")) + "/"
    rom_util.replace(rom_path , replacement_data_root, rom_path[:-4]+"_modified.nds", confirm=True)
elif choice == "1":
    # randomize
    print("### WIP RANDOMIZER ###")
    print("Drag and Drop your ROM in here or provide the path.")
    rom_path = input("> ")

    print("Please enter a seed (Numbers only or nothing for a random one!)")
    seed = input("> ")
    if seed == "":
        seed = random.randint(0, 65536)
    else:
        seed = int(seed)

    print("Choose one of three randomizer functions: (All of them are buggy lol)")
    print("There is a VERY high chance of softlocking the game regardless of setting :)")
    # Types:
    print("1 - nl -> no logic - completely random (probably the most interresting one)")
    print("2 - nld -> no logic dual - failed at linking two entrances together")
    print("3 - nll -> no logic linked - tries to link two entrances together but fails most of the time because it picks the wrong entrance (default)")
    print("4 - bl -> basic Logic (still work in progress)")
    
    randomizer_logic = input("> ")

    if randomizer_logic == "1":
        randoType = "nl"
    elif randomizer_logic == "2":
        randoType = "nld"
    elif randomizer_logic == "3":
        randoType = "nll"
    elif randomizer_logic == "4":
        randoType = "bl"    
    else:
        randoType = "nll"

    print("Your seed is: "+str(seed))
    print("Your randomizer type is: "+randoType)
    input("Press enter to start randomizing!")

    # Extract rom contents first!
    rom_util.extract(rom_path, "./extracted/root/", confirm=False)

    # Use the extracted files as randomizer input
    randomize.randomize(seed, "./extracted/root/Map/", "./extracted/randomized_"+randoType+"_"+str(seed)+"/Map/", randoType=randoType)

    # Reinsert the randomized files into a donor rom
    rom_util.replace(rom_path , "./extracted/randomized_"+randoType+"_"+str(seed)+"/", rom_path[:-4]+"_"+randoType+"_randomized_"+str(seed)+".nds", confirm=False)

    print("############################################################################################")
    print("############################################################################################")
    print("############################################################################################")
    print()
    print("All done!")
    print("Your seed is: "+str(seed))
    print("Your randomizer type is: "+randoType)
    print("You can find your ROM here: \"" + os.path.abspath(rom_path[:-4]+"_"+randoType+"_randomized_"+str(seed)+".nds") + "\"")
elif choice == "0":
    print("debug stuff:")
    print("1 - compare files")
    r = input("> ")
    if r == "1":
        f1 = input("File1> ")
        f2 = input("File2> ")
        b_f1 = d.ReadFile(f1)
        b_f2 = d.ReadFile(f2)
        if b_f1 == b_f2:
            print("Same files!")
        else:
            print("Different files!")
