import PyPDF2 as p
from Crypto.Cipher import AES
from Crypto.Random import random, new
import string
import os
import uuid
import hashlib

FILE_ATTRIBUTE_HIDDEN = 0x02

# UNUSED
def generate_random_password():
    password = ""
    for i in range(32):
        password += random.choice(list(string.printable.replace(' ', '')))
    return password

# UNUSED
def encrypt_password(password, encrypted_password_file):
    obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    ciphertext = obj.encrypt(password)
    f = open(encrypted_password_file, 'wb')
    f.write(ciphertext)
    
    f.close()

def encrypt_pdf(in_pdf, password):
    output = p.PdfFileWriter()
    input_stream = p.PdfFileReader(open(in_pdf, "rb"))

    for i in range(0, input_stream.getNumPages()):
        output.addPage(input_stream.getPage(i))

    out_pdf = in_pdf.split(".pdf")[0] + " (encrypted).pdf"
    outputstream = open(out_pdf, "wb")

    output.encrypt(password, use_128bit=True)
    output.write(outputstream)
    outputstream.close()

    os.remove(in_pdf)

def find_pdf():
    for file in os.listdir("."):
        if file.endswith(".pdf"):
            selection = input("Encrypt " + file + "? (y/n) ")
            if selection == "y":
                return file
    return False

def main():
    ret = find_pdf()
    if ret:
        in_pdf = ret
    else:
        print("No file selected. Aborting.")
        exit()

    password = hashlib.sha256(hex(uuid.getnode()).encode()).hexdigest()
    encrypt_pdf(in_pdf, password)
    # encrypt_password(password, ".enc")
    print("Encrypted!")


if __name__ == '__main__':
    main()