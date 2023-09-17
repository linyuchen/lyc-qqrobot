import sys
import tempfile
import time
import os
import os.path
from pathlib import Path


def is_gif(path) -> bool:
    try:
        file = open(path, "r+b")
        byte = file.read(3)
        file.close()
        return byte.decode() == "GIF"
    except:
        return False

def re_speed(path: Path, fps: int = 50) -> Path:
    fps = min(max(fps, 1), 50)
    interval = int(100 / fps)
    intervalBytes = interval.to_bytes(1, "little")

    try:
        if os.path.isfile(path):
            # print("Loading file: ", path, " ...")
            file = open(path, "r+b")
        else:
            raise Exception("The file was not found")

        byte = file.read(3)

        if byte.decode() != "GIF":
            raise Exception("Not a .gif")

        file.seek(0)
        fullFile = file.read()
        file.close()

        targetOut = tempfile.mktemp(suffix=".gif")
        # targetOut = os.path.splitext(path)[0] + "_reSpeed_" + str(fps) + ".gif"
        # for runOption in runOptions:
        #     if runOption == "-r":
        #         targetOut = path

        outFile = open(targetOut, "wb")
        outFile.write(fullFile)
        outFile.close()

        file = open(targetOut, "r+b")

        # print("ReSpeeding '", path, "' to a speed of", fps, "FPS...")

        while byte:
            if byte == b'\x21':
                byte = file.read(1)
                if byte == b'\xF9':
                    byte = file.read(1)
                    if byte == b'\x04':
                        file.seek(1, os.SEEK_CUR)
                        file.write(intervalBytes)
            byte = file.read(1)

    except Exception as e:
        file.close()
        raise e

    file.close()

    # for runOption in runOptions:
    #     if runOption == "-o":
    #         if sys.platform == "win32":
    #             os.startfile(targetOut)

    return Path(targetOut)


if __name__ == '__main__':

    fps = ""
    targetFile = ""
    runOptions = []

    print("GIF ReSpeed")
    print("Developed by LarsKDev")
    print("Version 1.0.3 | 5 Mar 2022")
    print("---------------------------")

    if len(sys.argv) == 1:
        targetFile = input("Please specify the location of the .gif file")
    elif len(sys.argv) > 1:
        targetFile = sys.argv[1]
        runOptions = sys.argv[2:]

    if len(sys.argv) > 2:
        print("Running with additional arguments", runOptions)

    while not isinstance(fps, int):
        try:
            fps = int(
                input("Please specify the new frame interval in frames per second: (GIF files only support up to 50 fps)"))
        except:
            print("Please enter a valid integer")

    folderOption = False
    for runOption in runOptions:
        if runOption == "-f":
            folderOption = True
            print("Converting all .gifs in folder...")
            if os.path.isdir(targetFile):
                targetFiles = os.listdir(targetFile)

                for f in targetFiles:
                    re_speed(targetFile + "/" + f, fps)
            else:
                print("Please specify a folder...")

    if not folderOption:
        re_speed(targetFile, fps)

    time.sleep(2)