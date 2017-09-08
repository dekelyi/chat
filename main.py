from _client.main import MainConnection
from _client.log import LogConn
from _client.prompt import PromptConn
import utils


def main():
    conn = MainConnection((utils.my_address(), 7000))
    conn.add_connection(LogConn)
    conn.add_connection(PromptConn)
    conn.main()

main()
