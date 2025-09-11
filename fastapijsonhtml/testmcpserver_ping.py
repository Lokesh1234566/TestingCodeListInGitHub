import socket


def test_connection(host="localhost", port=8000, timeout=2):
    try:
        print("Inside Test_connection")
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (OSError, ConnectionRefusedError, TimeoutError):
        return False


def main():
    print("Hello ping test")
    if test_connection("localhost", 8000):
        print("Port 8000 is open and reachable ✅")
    else:
        print("Port 8000 is closed or unreachable ❌")

    test_connection()


if __name__ == "__main__":
    main()
