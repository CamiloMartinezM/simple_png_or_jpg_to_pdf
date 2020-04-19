# -*- coding: utf-8 -*-
import os
import shutil
import sys
from os import name
from pathlib import Path
from typing import Tuple

import img2pdf
from PIL import Image

import give_console_width

# Console width of the current/active console.
CONSOLE_WIDTH = give_console_width.main()

# Title of the program.
TITLE = "Hi! Welcome to your Image to PDF converter!"

# Developer.
THANKS_TO = "Developed by Camilo Martínez"

def clear() -> None:
    """ Clears the console.
    """
    if name == 'nt':
        _ = os.system('cls')  # For windows.
    else:
        _ = os.system('clear')  # For mac and linux (here, os.name is 'posix').

def show_introduction() -> None:
    """ Shows introduction of the program.
    """
    print("~" * CONSOLE_WIDTH)
    print("")
    print(" " * int(str((CONSOLE_WIDTH - len(TITLE))//2)) +
          TITLE + " " * int(str((CONSOLE_WIDTH - len(TITLE))//2)))
    print(" "*(int(CONSOLE_WIDTH*2-len(THANKS_TO)-3)), end="")
    print(THANKS_TO)
    print("~" * CONSOLE_WIDTH)
    print("")
    
class ImageToPDFConverter:

    def __init__(self, filename: str, directory: str, png_or_jpg: Tuple[bool]) -> None:
        self.filename = filename
        self.directory = directory
        self.fullpath_to_file = ImageToPDFConverter.join(directory, filename)

        self.get_png = png_or_jpg[0]
        self.get_jpg = png_or_jpg[1]

        self.new_files_created = list()
        self.images = self.get_images()

    def get_images(self) -> None:
        images = list()

        for i in os.listdir(self.directory):
            path_i = self.join(self.directory, i)
            i_original_filename = os.path.basename(i)

            if i.endswith(".jpg"):
                if self.get_jpg:
                    print("[+] Appending " + i_original_filename)
                    images.append(path_i)
            elif i.endswith(".png"):
                if self.get_png:
                    try:
                        print("[+] Found " + i_original_filename + ". Attempting conversion to .jpg... ", end="")
                        images.append(self.deal_with_png(self.directory, i_original_filename))
                        print("Done!")
                    except:
                        print("\n\n[*] There was a problem with " + i_original_filename + ". Skipping...")

        return images

    def filter_images(self, images: list) -> list:
        filtered = list()

        for i in range(len(images)):
            print("[+] Testing if " + os.path.basename(images[i]) + " can be converted to pdf... ", end="")
            path_i = self.join(self.directory, "t" + str(i) + ".pdf")
            with open(path_i, "wb") as f1:
                f1.write(img2pdf.convert(bytes(images[i], 'utf-8')))
                filtered.append(images[i])
                print("Affirmative!")

            os.remove(self.join(self.directory, "t" + str(i) + ".pdf"))

        return filtered

    @classmethod
    def join(cls, directory: str, f: str) -> str:
        return os.path.join(directory, f).replace("\\", "/")

    def deal_with_png(self, path, name) -> str:
        new_name = self.png_to_jpg(self.join(path, name))
        self.new_files_created.append(self.join(self.directory, new_name))
        return self.join(self.directory, new_name)

    @classmethod
    def png_to_jpg(cls, img) -> str:
        new_name = img.split(".")[0] + "_converted.jpg"
        im = Image.open(img).convert("RGB")
        im.save(new_name, "jpeg")
        return new_name

    def create_pdf(self) -> int:
        with open(self.fullpath_to_file, "wb") as f:
            if not self.images:
                print("[*] Not a single .jpg or .png file was found in " + self.directory + ".")
                f.close()
                os.remove(self.join(self.directory, self.filename))
            else:
                print("")
                filtered_images = self.filter_images(self.images)

                if not filtered_images:
                    print("[*] None of the images could be converted to pdf, so there is no output pdf file.")
                    return None
                else:
                    f.write(img2pdf.convert(filtered_images))
                    f.close()
                    shutil.move(self.fullpath_to_file, self.join(os.getcwd(), self.filename))

                for file_ in self.new_files_created:
                    os.remove(self.join(self.directory, file_))

        return 1
    
    @classmethod
    def check_if_shrinkpdf_exists(cls, directory):
        shrinkpdf_exists = False
        for f in os.listdir(os.getcwd()):
            if os.path.basename(f) == "shrinkpdf.bat":
                shrinkpdf_exists = True

        return shrinkpdf_exists

    def compress_pdf(self, dpi: str) -> int:
        from subprocess import Popen, PIPE
        p = Popen([self.join(os.getcwd(), "shrinkpdf.bat"), \
                                "-dpi", dpi.strip(), \
                                self.filename], shell=True, stdout=PIPE)

        for line in p.stdout:
            print("\n[+] " + line.decode('utf-8').strip()[1:-1])

        for f in os.listdir(os.getcwd()):
                if os.path.basename(f) == self.filename:
                    os.rename(os.path.basename(f), os.path.basename(f)[:-4] + "_original.pdf")
                    break

        os.rename("output.pdf", self.filename)

        shutil.move(os.path.join(os.getcwd(), self.filename), self.fullpath_to_file)
        shutil.move(os.path.join(os.getcwd(), self.filename[:-4] + "_original.pdf"), self.join(self.directory, self.filename[:-4] + "_original.pdf"))

def exit_() -> None:
    input("\n[+] Press any key to exit...")
    print("")
    clear()
    sys.exit(0)

def main():
    clear()

    show_introduction()

    directory = input("[?] Use current directory (any letter) or Desktop (press Enter): ")

    raw_option = "0"
    while raw_option.strip() not in ["", "1", "2"]:
        raw_option = input("[?] Use only jpg's (press Enter), only png's (1) or all (2): ")

    if raw_option == "":
        option = (False, True)
    elif raw_option == "1":
        option = (True, False)
    else:
        option = (True, True)

    if directory == "":
        try:
            directory = os.path.expanduser("~/Desktop")
        except:
            try:
                directory = os.path.expanduser("~/Escritorio")
            except:
                print("\n[*] There was a problem finding the desktop folder.")
                exit_()
    else:
        directory = os.getcwd()

    directory = directory.replace("\\", "/")
    output_filename = input("[?] Name of output file (press Enter for default: out): ")

    if output_filename == "":
        output_filename = "out.pdf"
    elif not output_filename.endswith(".pdf"):
        output_filename += ".pdf"
    elif "." in output_filename:
        dot_split = output_filename.split(".")
        output_filename = dot_split[0]

    print("\n[+] Converting images to PDF...\n")

    converter = ImageToPDFConverter(output_filename, directory, option)
    
    try:
        r = converter.create_pdf()
        if r is None:
            exit_()
    except SystemExit:
        sys.exit(0)
    except:
        print("\n[*] There was an unexpected error with the inputted filename. Default filename will be used.\n")

        converter = ImageToPDFConverter("out.pdf", directory, option)

        try:
            r2 = converter.create_pdf()
            if r2 is None:
                exit_()
        except SystemExit:
            sys.exit(0)
        except:
            print("\n[*] An unexpected error ocurred...")
            exit_()

    print("\n[+] Conversion successful!\n")

    shrinkpdf_exists = ImageToPDFConverter.check_if_shrinkpdf_exists(converter.directory)

    if shrinkpdf_exists:
        print("[+] There is .bat file called shrinkpdf in the current directory.")
        raw_compress = input("[?] Perform PDF compression with ghostscript (press Enter if 'yes', type anything else for 'no'): ")

        if raw_compress.strip() == "":
            compress = True
        else:
            compress = False
        
        if compress:
            dpi = input("[?] Specify dpi (press Enter if default is to be used: 72): ")

            if dpi == "":
                dpi = "72"
            else:
                repeat = True
                while repeat:
                    try:
                        int_dpi = int(dpi.strip())
                        if int_dpi <= 0:
                            continue
                        
                        repeat = False
                        del int_dpi
                    except:
                        print("[*] Invalid entry!")
                        dpi = input("[?] Specify dpi (press Enter if default is to be used: 72): ")
                        repeat = True

            converter.compress_pdf(dpi)
        else:
            exit_()
            sys.exit(0)

    exit_()

if __name__ == "__main__":
    main()
