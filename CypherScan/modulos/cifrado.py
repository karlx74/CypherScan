import os

def encrypt_cesar(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalnum():
            if char.isalpha():
                shifted = ord(char) + shift
                if char.islower():
                    if shifted > ord('z'):
                        shifted -= 26
                    elif shifted < ord('a'):
                        shifted += 26
                elif char.isupper():
                    if shifted > ord('Z'):
                        shifted -= 26
                    elif shifted < ord('A'):
                        shifted += 26
                encrypted_text += chr(shifted)
            elif char.isdigit():
                shifted = int(char) + shift
                if shifted > 9:
                    shifted -= 10
                encrypted_text += str(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def save_encrypted_text(encrypted_text, file_path):
    with open(file_path, 'w') as file:
        file.write(encrypted_text)

def encrypt_files_in_folder(folder_path, shift):
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            file_path = os.path.join(root, name)
            if file_path.endswith('.txt'):
                with open(file_path, 'r') as file:
                    text = file.read()
                encrypted_text = encrypt_cesar(text, shift)
                save_encrypted_text(encrypted_text, file_path.replace('.txt', '_cifrado.txt'))

def cifrar_archivos():
    carpeta_metadatos = r"C:\Users\karla\OneDrive\Documentos\GitHub\CypherScan\modulos\metadatos"
    shift = 3
    encrypt_files_in_folder(carpeta_metadatos, shift)
