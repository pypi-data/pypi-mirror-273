import argparse
from .PingDing import constructMainWindow

def main():
    parser = argparse.ArgumentParser(prog="PingDing", description="Ping various IPs")
    parser.add_argument('tMax', help="at this time the box will be totally red", type=int)
    parser.add_argument('addr', nargs="*")

    constructMainWindow(float(parser.parse_args().tMax), parser.parse_args().addr)
    