from _client.main import MainConnection
from _client.connection import Connection
import utils


def main():
    conn = MainConnection((utils.my_address(), 7000))
    conn.add_connection(Connection)
    conn.main()

main()
