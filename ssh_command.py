#!/usr/bin/python2.7
from events import *
from jobs import *
import threading
import Queue
import getopt
import getpass
import sys

def main(argv):
    queueLock = threading.Lock()
    workQueue = Queue.Queue()
    threads = []
    server_list = []
    try:
        opts, args = getopt.getopt(argv, "hs:ilxp:c:", ["help", "list" ,"server=", "src=", "add", "idc=", "command="])
    except getopt.GetoptError:
        print "arg error"
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--idc"):
            proxy_file = arg
        elif opt in ("-s", "--src"):
            server_list_file = arg
        elif opt in ("-c", "--command"):
            command = arg

    ssh_config = paramiko.SSHConfig()
    ssh_config.parse(open(proxy_file))
    password = getpass.getpass("Enter password: ")

    file_object = open(server_list_file, 'r')
    for line in file_object:
        server_list.append(line.strip())

    finnal_list = Events(server_list, 10).handle_list()

    for onces in finnal_list:
        for server in onces:
            thread = ThreadJob(workQueue, server, 51022, password, ssh_config, command)
            thread.start()
            threads.append(thread)

    for t in threads:
        t.join()

    while not workQueue.empty():
        a = workQueue.get()
        print a[0]['WlanIp']
        print a[0]['Message']

if __name__ == '__main__':
    main(sys.argv[1:])
