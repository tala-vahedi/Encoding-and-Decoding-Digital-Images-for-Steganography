# Script Purpose: Covert Communications With Python
# Script Version: 1.0 
# Script Author:  Tala Vahedi

# Script Revision History:
# Version 1.0 Oct 27, 2021, Python 3.x


''' 3rd Party Library '''
from PIL import Image               # pip install pillow
import os
import numpy as np

# Script Constants
SCRIPT_NAME    = "Script: Covert Communications With Python"
SCRIPT_VERSION = "Version 1.0"
SCRIPT_AUTHOR  = "Author: Tala Vahedi"

# function that performs the hiding of the msg
def encoder(fileDir, msg, outputDir):
    # opening the file
    img = Image.open(fileDir, 'r')
    # getting the image size
    w, h = img.size
    print("old img size:", w, h)

    # converting the image into an array of pixels
    lst = np.array(list(img.getdata()))
    # getting the image mode (e.g., RGB or RGBA)
    imgMode = img.mode
    # getting length of image tuple
    tupleLen = len(imgMode)

    # converting the msg into byte format
    msgByes = ''.join([format(ord(i), "08b") for i in msg])

    # initializing an interable variable
    i=0
    # looping through all tuples in the image
    for pix in range((lst.size//tupleLen)):
        # looping through the red/blue/green pixels
        for mode in range(0, 3):
            # if we are still within the confines of the image size
            if i < len(msgByes):
                # convert one bit within the array of pixels
                lst[pix][mode] = int(bin(lst[pix][mode])[2:9] + msgByes[i], 2)
                # increment the size by 1
                i += 1

    # once pixel is changed, update the array
    array = lst.reshape(h, w, tupleLen)
    # convert it back into a regular image
    encodedImg = Image.fromarray(array.astype('uint8'), img.mode)
    # save the file to directory based on user's output file name
    if '.bmp' not in outputDir:
        encodedImg.save(outputDir + '.bmp')
        print("\npixel steganography for", fileDir, "is complete\n")
    else:
        encodedImg.save(outputDir)
        print("\npixel steganography is complete\n")
    print("new img size:", w, h)

if __name__ == '__main__':
    # print basic script info
    print()
    print(SCRIPT_NAME)
    print(SCRIPT_VERSION)
    print(SCRIPT_AUTHOR)
    print()

    # creating a dictionary to hold the messages for encoding
    codes = {}
    with open("CodeBook.txt") as f:
        for line in f:
            (key, value) = line.split(" ", 1)
            codes[int(key)] = value.strip()
    
    try:
        # prompting the user for a directory path continoulsy 
        while True:
            # prompting user to enter a path or enter 'exit' to end the program
            fileDir = input("Please enter image filename or enter 'exit' to quit program: ")
            # condition that ends the program if user inputs 'exit'
            if fileDir == "exit":
                exit()
            # if path is not found, prompt the user to re-enter a path or exit the program
            elif os.path.exists(fileDir) == False:
                print("\nERROR: invalid file path, please try another path\n")
                continue
            # print processing the file path and break while statement to continue with code
            else:
                print("\nImage found, processing file...\n")
                # prompting user for valid input of message
                while True:
                    # try except to catch errors and repeat while
                    try:
                        # iterating through dictionary items and printing out possible messages
                        for key, value in codes.items():
                            print(key,": ", value)
                        # getting the user input for their selected message
                        msgKey = int(input("\nPlease select one message from the list above to encode in the image: "))                        
                        # if user selected correct message number
                        if msgKey in codes.keys():
                            print("\nProcessing request, please wait...")
                            # grab the associated message
                            msg = codes[msgKey]
                            # ask for a user output file name
                            outputDir = input("\nPlease enter a file output name: ")
                            # call the encoder function with the file name, the msg, and the out file name 
                            encoder(fileDir, msg, outputDir)
                            # break out iteration
                            break
                        else:
                            # otherwise raise a value error of user's input
                            raise ValueError("\nERROR: message not found\nPlease select a number from list below:")

                    # raise another value error
                    except ValueError:
                        print("\nERROR: message not found\nplease select a message from the list below")
    
    # raise another exception
    except Exception as err:
        print("Steg Failed: ", str(err))