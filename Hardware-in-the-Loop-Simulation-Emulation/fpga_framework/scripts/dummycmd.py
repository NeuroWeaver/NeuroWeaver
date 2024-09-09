'''
Program takes in input time in seconds, sleeps for specified amount of time and returns
'''
import argparse
import time

parser = argparse.ArgumentParser(description='dummy cmd to run for x amount of seconds')
parser.add_argument('--time', type=int)
args = parser.parse_args()

time.sleep(args.time)