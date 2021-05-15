import os
import ndspy.rom
import hashlib

def extract(rom_path, e_path, confirm=True):
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    print(rom)
    # print(rom.filenames)

    output = e_path

    if confirm:
        inp = input("Extract ROM Contents to \"" + os.path.abspath(output) + "\"? [y/n]")
        if inp != "y":
            print("Extraction cancelled!")
            return

    for i, file in enumerate(rom.files):
        try:
            rom_internal_file_name = rom.filenames[i]
            # print(rom_internal_file_name)

            path_wf = output + rom_internal_file_name
            path = path_wf[:len(path_wf)-len(os.path.basename(path_wf))]

            # print(path_wf)
            # print(path)

            try:
                os.makedirs(path)
            except FileExistsError:
                # directory already exists
                pass

            if not os.path.isfile(path_wf):
                with open(path_wf, 'w+b') as f:
                    f.write(file)
                print("[Extracted] " + rom_internal_file_name + " -> " + path_wf)
            else:
                print("[Skipped] " + rom_internal_file_name + " // " + path_wf)

        except KeyError:
            print("[Ignored] ID " + str(i) + " has no filename!")

# if only_modified is set to True, both files will be hashed and only replaced if the hashes differ!
def replace(rom_path, i_path, save_path, confirm=True, only_modified=False):
    # Re-inserts files!
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    print(rom)

    if confirm:
        inp = input("Insert ROM Contents from \"" + os.path.abspath(i_path) + "\" into \"" + os.path.abspath(rom_path) + "\" and save to file \"" + os.path.abspath(save_path) + "\"? [y/n]")
        if inp != "y":
            print("Insertion cancelled!")
            return

    for i, file in enumerate(rom.files):
        try:
            rom_internal_file_name = rom.filenames[i]
            #print(rom_internal_file_name)

            path_wf = i_path + rom_internal_file_name

            #print(path_wf)

            if os.path.isfile(path_wf):
                with open(path_wf, 'rb') as f:
                    bin_file = f.read()

                    if only_modified:
                        h = hashlib.md5(bin_file).hexdigest()
                        h_romfile = hashlib.md5(file).hexdigest()

                        if not (h == h_romfile):
                            # Replace File!
                            rom.setFileByName(rom_internal_file_name, bin_file)
                            print("[Inserted] " + rom_internal_file_name + " <- " + path_wf)
                        else:
                            pass
                            #print("File hasn't been modified!")
                    else:
                        rom.setFileByName(rom_internal_file_name, bin_file)
                        print("[Inserted] " + rom_internal_file_name + " <- " + path_wf)
            else:
                pass
                #print("File skipped - File doesn't exist!")

        except KeyError:
            print("[Ignored] ID " + str(i) + " has no filename!")

    print("Saving rom...")
    with open(save_path, 'wb') as f:
        f.write(rom.save())
    print("Done!")

if __name__ == "__main__":
    # extract("../../DS/zph.nds" , "../out/", confirm=False)
    replace("../../DS/zph.nds" , "../../DS/randomize/data/", "../zph_mod.nds", confirm=False) # , confirm=False