import socket
import string
import re

FRAME_REGEX = re.compile(r"frame=\d+ bb=\[\d+,\d+,\d+,\d+\] AR=\d+\.\d+")

def listen_scamp5_proxy(ip="127.0.0.1", port=27888):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    print("[SUCCESS] Connected to SCAMP5 proxy")

    buffer = ""
    try:
        while True:
            data = s.recv(1024)
            if not data:
                break

            decoded = data.decode("utf-8", errors="ignore")
            buffer += decoded

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()

                match = FRAME_REGEX.search(line)
                if match:
                    clean_text = match.group()
                    print("[SCAMP5]", clean_text)
                    with open('frames_clean.txt', 'a') as f:
                        f.write(clean_text + "\n")

    except KeyboardInterrupt:
        print("Interrupted.")
    finally:
        s.close()


def main():
    listen_scamp5_proxy()

if __name__ == '__main__':
    main()
