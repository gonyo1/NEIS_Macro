import socket


def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    지정된 호스트와 포트에 소켓 연결을 시도하여 인터넷 연결 여부를 확인합니다.

    기본적으로 Google의 DNS 서버(8.8.8.8:53)에 연결을 시도합니다.
    """
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
        return True
    except socket.error:
        return False
