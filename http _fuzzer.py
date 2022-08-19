import os
import argparse
import subprocess
import requests
import time
parser = argparse.ArgumentParser(description='Network Http Fuzzer made by Akshat Parikh (Please install Radamsa and use linux)')
parser.add_argument('-P', '--process', help = "Specify http server process id", required=True)
parser.add_argument('-N', '--number', help = "Number of times you want to use fuzzer", required=True)
parser.add_argument('-H', '--host', help = "Host", required=True)
parser.add_argument('-M', '--port', help = "Host Port", required=True)
parser.add_argument('-I', '--input', help = "Input Directory", required=True)
parser.add_argument('-O', '--output', help = "Output directory", required=True)
args = parser.parse_args()
counter = 0
files = os.listdir(args.input)
crash = 0
while counter < int(args.number):
    if crash == 0:
        for x in range(len(files)):
            pslist = subprocess.check_output("ps -A -o pid", shell=True)
            if (str(args.process) in str(pslist)) == True:
                print("active")
                time.sleep(1)
                testcase = os.popen("cat "+ args.input+files[x] + " | radamsa > "+args.output+"testcase"+str(x)).read()
                print(counter)
                try:
                    request = subprocess.check_output("nc "+ args.host+" "+args.port+" < "+args.output+"testcase"+str(x),stderr=subprocess.STDOUT, timeout=5, shell=True)
                except subprocess.TimeoutExpired:
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    os.system("cp "+args.output+"testcase"+str(x)+" "+args.output+current_time+"Hang")
                    print("Interesting Case/Hang Detected")
                print(request)
            else:
                print("crash detected check timestamp in logs")
                crash = 1
                break
        counter += 1
    else:
        break
