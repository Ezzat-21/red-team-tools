import socket

IP = '192.168.56.104'
PORT = 21

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)
result = s.connect_ex((IP, PORT))

if result == 0:
    banner = s.recv(1024).decode().strip()
    print(f"Connected: {banner}")

    s.send(b"USER anonymous\r\n")
    response = s.recv(1024).decode().strip()
    print(f"USER response: {response}")

    if '331' in response:
        s.send(b"PASS anonymous@\r\n")
        response2 = s.recv(1024).decode().strip()
        print(f"PASS response: {response2}")

        if '230' in response2:
            print("[+] Anonymous FTP login allowed!")
            s.send(b"STOR test_upload.txt\r\n")
            response3 = s.recv(1024).decode().strip()
            print(f"STOR response: {response3}")

            if '550' in response3:
                print("[-] Upload not allowed")
            elif '125' in response3 or '150' in response3:
                print("[+] Upload allowed — critical vulnerability")
            else:
                print(f"[?] Unexpected response: {response3}")
        else:
            print("[-] Anonymous login denied")
    else:
        print("[-] Server did not ask for password")
else:
    print("[-] Port 21 closed")

s.close()