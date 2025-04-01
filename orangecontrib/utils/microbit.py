import serial
import time
import serial.tools.list_ports

_connection = None


def list_ports() -> list:
    """사용 가능한 시리얼 포트 목록 반환"""
    return [port.device for port in serial.tools.list_ports.comports()]


def connect(port: str, baudrate: int = 115200, timeout: float = 1.0) -> str:
    """포트에 연결 시도. 성공 시 포트명 반환."""
    global _connection
    if _connection:
        _connection.close()
    _connection = serial.Serial(port, baudrate=baudrate, timeout=timeout)
    time.sleep(2)  # 연결 안정화 대기
    return _connection.port


def disconnect():
    """연결 해제"""
    global _connection
    if _connection and _connection.is_open:
        _connection.close()
        _connection = None


def is_connected() -> bool:
    """현재 연결 여부 반환"""
    global _connection
    return _connection is not None and _connection.is_open


def send_and_receive(message: str, wait_time: float = 1.0) -> str:
    """메시지 전송 후 응답 수신"""
    global _connection
    if not _connection or not _connection.is_open:
        raise RuntimeError("Microbit 연결이 되어 있지 않습니다. connect(port)를 먼저 호출하세요.")

    _connection.write((message + '\n').encode('utf-8'))
    time.sleep(wait_time)
    response = _connection.readline().decode('utf-8').strip()
    return response