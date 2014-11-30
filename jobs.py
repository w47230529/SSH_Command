import paramiko
import threading
import time

class RemoteJobs:
    def __init__(self, Queue, UserName, Password, ssh_config):
        import paramiko
        self.UserName = UserName
        self.Password = Password
        self.queue = Queue
        self.result_list = []
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.conf = ssh_config
        # self.conf.parse(open(proxy_file))

    def remote_command(self, server, port, command):
        self.Report = {}
        host = self.conf.lookup(server)
        proxy = paramiko.ProxyCommand(host['proxycommand'])
        #proxy = paramiko.ProxyCommand("nc -X 5 -x 127.0.0.1:7080 %s 51022" % server)
        try:
            self.ssh.connect(server ,port=port ,username=self.UserName ,\
                                password=self.Password ,timeout=3 ,sock=proxy)
            #self.ssh.connect(server ,port=port ,username=self.UserName ,\
            #                    password=self.Password ,timeout=3)
        except:
            self.Report["WlanIp"] = server
            self.Report["Status"] = "Failed"
            self.Report["Message"] = "Connect Failed !"
            self.result_list.append(self.Report)
        else:
            # stdin, stdout, stderr = self.ssh.exec_command('%s' % "grep 'GATEWAY' /etc/sysconfig/network-scripts/ifcfg-*")
            # stdin, stdout, stderr = self.ssh.exec_command('%s' % "grep 'GATEWAY' /etc/sysconfig/network")
            # stdin, stdout, stderr = self.ssh.exec_command('%s' % "grep 'nameserver' /etc/resolv.conf")
            # stdin, stdout, stderr = self.ssh.exec_command('%s' % "cat /tmp/modifyNetwork.logs")
            stdin, stdout, stderr = self.ssh.exec_command('%s' % command)
            self.Report["WlanIp"] = server
            if stdout.channel.recv_exit_status() == 0:
                self.Report["Status"] = "Successfully"
                self.Report["Message"] = stdout.read()
            else:
                self.Report["Status"] = "Failed"
                self.Report["Message"] = stderr.read()
            self.result_list.append(self.Report)
        finally:
            self.queue.put(self.result_list)
            self.ssh.close()

class ThreadJob(threading.Thread):
    def __init__(self, queue, server, port, password, proxy_file, cmd):
        threading.Thread.__init__(self)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        self.server = server
        self.port = port
        self.password = password
        self.cmd = cmd
        self.queue = queue
        self.proxy_file = proxy_file
        threads = []

    def run(self):
        Shell=RemoteJobs(self.queue, 'wangyazhe', self.password, self.proxy_file)
        threadLock = threading.Lock()
        # print "Starting " + self.server
        threadLock.acquire()
        Shell.remote_command(self.server, self.port, self.cmd)
        threadLock.release()
