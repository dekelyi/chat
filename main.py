from _client.main import MainConnection
from _client.log import LogConn
import utils


def main():
    conn = MainConnection((utils.my_address(), 7000))
    conn.add_connection(LogConn)
    conn.main()

main()
