from Crypto.Cipher import AES
import PyPDF2 as p
import uuid 
import hashlib
import os

def decrypt_password(encrypted_password_file):
    f = open(encrypted_password_file, 'rb')
    ciphertext = f.read()
    obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    return obj.decrypt(ciphertext)

def decrypt_pdf(input_path, password):
    output_path = "".join(input_path.split(" (encrypted)"))
    with open(input_path, 'rb') as input_file, \
        open(output_path, 'wb') as output_file:
        reader = p.PdfFileReader(input_file)
        reader.decrypt(password)

        writer = p.PdfFileWriter()

        for i in range(reader.getNumPages()):
            writer.addPage(reader.getPage(i))

        writer.write(output_file)

    os.remove(input_path)

def find_pdf():
    for file in os.listdir("."):
        if file.endswith(".pdf"):
            selection = input("Decrypt " + file + "? (y/n) ")
            if selection == "y":
                return file
    return False

def main():
    ret = find_pdf()
    if ret:
        out_pdf = ret
    else:
        print("No file selected. Aborting.")
        exit()

    # password = decrypt_password(".enc").decode()
    # print(password)
    password = hashlib.sha256(hex(uuid.getnode()).encode()).hexdigest()
    decrypt_pdf(out_pdf, password)
    print("Decrypted!")


if __name__ == '__main__':
    main()