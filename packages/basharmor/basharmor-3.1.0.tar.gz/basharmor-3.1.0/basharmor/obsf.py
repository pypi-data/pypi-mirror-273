def encrypt(text):
    encrypted_text = ""
    for char in text:
        encrypted_text += chr(ord(char) + 1000000)   
    return encrypted_text

def decrypt(encrypted_text):
    decrypted_text = ""
    for char in encrypted_text:
        decrypted_text += chr(ord(char) - 1000000)
    return decrypted_text

def encrypt_file(input_file, output_file):
    with open(input_file, "r") as file:
        script_content = file.read()
    
    encrypted_content = encrypt(script_content)  

    with open(output_file, "w") as file:
        file.write(encrypted_content)

    return encrypted_content

def decrypt_file(input_file):
    with open(input_file, "r") as file:
        encrypted_content = file.read()

    decrypted_content = decrypt(encrypted_content)  
    return decrypted_content


