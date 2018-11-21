
#  This is a Python Program whose objective is to encode and decode text in/from an image

import PIL.Image

from tkinter import filedialog, Toplevel
from tkinter import *
import os
import shutil


# Converting text into 8-bit binary from using ASCII value of characters
def genBinary(data):
    # Function generates binary codes
    list = []

    for i in data:
        list.append(format(ord(i), '08b'))
    return list


def modPixel(pix, data):
    #pixels are modified according to the binary list version of the encoded text/data
    datalist = genBinary(data)
    lengthdata = len(datalist)
    imgdata = iter(pix)

    for i in range(lengthdata):

        # Taking 3 pixels at a time
        pix = [value for value in imgdata.__next__()[:3] +
               imgdata.__next__()[:3] +
               imgdata.__next__()[:3]]

        # Pixel value are made odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

                if (pix[j] % 2 != 0):
                    pix[j] -= 1

            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                pix[j] -= 1

        # Eighth pixel is used to check whether the generated encoded data needs to be read or not
        if (i == lengthdata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] -= 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encoder(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPixel(newimg.getdata(), data):

        # Inserting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


# Encoding data/text into image
def encode(data):
    root = Tk()
    root.iconify()
    x1 = data
    if (x1 != ''):
        x = filedialog.askopenfilename(initialdir="/", title="Select file",
                                       filetypes=(('image files', ('.png', '.jpg')), ("all files", "*.*")))
        y = os.path.split(x)[1]
        y1 = y.split(".")
        shutil.copy(x, '/Users/RAGHAV VERMA/.PyCharm2018.2/config/scratches')

        image = PIL.Image.open(y, 'r')
        if (len(x1) == 0):
            raise ValueError('Data is empty')

        newimg = image.copy()
        encoder(newimg, x1)

        new_img_name = y1[0] + "-encoded.png"
        newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))


# Decoding the data from given image from file explorer
def decode():
    window = Tk()
    window.iconify()
    x = filedialog.askopenfilename(initialdir="/", title="Select file",
                                   filetypes=(('image files','*.png'), ("all files", "*.*")))

    y = os.path.split(x)[1]
    image = PIL.Image.open(y, 'r')
    x1 = ''
    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]
        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data
        # Main Function

#Function for receiving the entered text (in the GUI) and passing it as a argument to the encoding function
def click1(data):
    inputtext = data.get("1.0", "end-1c")
    encode(inputtext)

#Seperate Window to display the decoded text with word wrapping properties
def messageWindow(x2,window):
    #Top Level is used to display the window at the very front in case there is already a seperate window open as reference
    win = Toplevel()
    #To restrict window geometrical size
    win.resizable(width=False, height=False)
    #To remove the unnecessary Tk() window
    win.iconify()

    win.title("Decoded Text")
    #Hex code for dark blue
    win.configure(background="#192a3d")
    Label(win, text="Decoded Text:\n", bg="#192a3d", fg="white", font=("MarvelScript", 12, "bold")).grid(row=1,
                                                                                                   column=0,
                                                                                                   sticky="N")
    Label(win, text=x2, bg="black", fg="white", font=("Sitka", 12, "bold"),wraplength=1600 ).grid(row=2,
                                                                             column=0,
                                                                             sticky="N")
    Button(win, text="Exit", width=4, command=lambda: win.destroy()).grid(row=3, column=0, sticky="E")
#Receives the GUI Window and a variable for text as arguments and passes through decode function
def click2(x2, window):
    x2 = decode()
    messageWindow(x2,window)

#To close the present window
def close_window(window):
    window.destroy()
    exit()


def main():
    x2 = ""
    window = Tk()
    window.iconify()
    #Main Window Layout
    window.title("Steganographic Decoder/Encoder")
    window.configure(background="black")
    window.geometry("455x350")
    window.resizable(width=False, height=False)
    photo1 = PhotoImage(file="Untitled-1.png")
    Label(window, image=photo1, bg="black").grid(row=0, column=0, sticky="W")
    Label(window, text="Enter text that you want to encode", bg="black", fg="white", font=("Calibri", 12)).grid(row=4,
                                                                                                                column=0,
                                                                                                                sticky="N")
    #Variable for Text Entry in GUI
    data = Text(window, height=1, width=55)
    data.grid(row=5, column=0, sticky="W")

    Button(window, text="Encode", width=6, command=lambda: click1(data)).grid(row=5, column=0, sticky="E")

    Label(window, text="\nSelect an Image to decode text with", bg="black", fg="white", font=("Calibri", 12)).grid(
        row=8,
        column=0,
        sticky="N")
    Label(window, text="", bg="black", fg="white", font="none 12 bold").grid(row=11,
                                                                             column=0,
                                                                             sticky="N")
    Button(window, text="Decode Image", width=11, command=lambda: click2(x2, window)).grid(row=11, column=0, sticky="N")

    Label(window, text="", bg="black", fg="white", font=("Calibri", 12, "bold")).grid(row=13,
                                                                                      column=0,
                                                                                      sticky="N")
    Label(window, text="", bg="black", fg="white", font=("Calibri", 12, "bold")).grid(row=14,
                                                                                      column=0,
                                                                                      sticky="N")
    Label(window, text="", bg="black", fg="white", font=("Calibri", 12, "bold")).grid(row=15,
                                                                                      column=0,
                                                                                      sticky="N")
    Label(window, text="", bg="black", fg="white", font=("Calibri", 12, "bold")).grid(row=16,
                                                                                      column=0,
                                                                                      sticky="N")
    Button(window, text="Exit", width=4, command=lambda: close_window(window)).grid(row=17, column=0, sticky="E")
    window.mainloop()


if __name__ == '__main__':
    # Calling main function
    main()