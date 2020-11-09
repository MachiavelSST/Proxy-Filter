import sys, os, argparse, threading, time
from proxy_checker import ProxyChecker

argparser = argparse.ArgumentParser()
argparser.add_argument('filename',help = 'Input filename')
argparser.add_argument('threads',help = 'Threads')
args = argparser.parse_args()
try:
	args.threads  = int(args.threads)
except TypeError:
	print("Threads must be an integer")
	sys.exit(1)
	

class MyProxyChecker(threading.Thread):
	
	def __init__(self, arrLinks, threadId):
		threading.Thread.__init__(self)
		self.arrLinks = arrLinks
		self.threadId = threadId
		
	def run(self):
		global counter, length
		checker = ProxyChecker()
		for i, line in enumerate(self.arrLinks):
			resp = checker.check_proxy(line)
			counter = counter + 1
			if resp and (resp["anonymity"] == "Elite" or resp["anonymity"] == "Anonymous"):
				print("{0}/{1} Proxy -> {2} is VALID".format(counter,len(lines),line))
				f=open("valid.txt","a")
				f.write(line+"\n")
				f.close()
			else:
				print("{0}/{1} Proxy -> {2} is NOT VALID".format(counter,len(lines),line))
			


def readFile(filename):
	array = []
	if not fileExist(filename): return array
	with open(filename) as f:
		for line in f:
			array.append(line.replace("\n", "").strip())
		f.close()
		
	return array

def fileExist(f):
	if os.path.isfile(f):
		return True
	else:
		return False


# main
lines = readFile(args.filename)
if args.threads > (len)(lines): args.threads = (len)(lines)

perThread = (int)((len)(lines) / args.threads)
perThreadModule = (int)((len)(lines) % args.threads)
threadsArr = []
counter = 0
length = (len)(lines)

for i in range(args.threads):
	st = i*perThread
	end = i*perThread+perThread
	
	if (i+1) == args.threads: end = end + perThreadModule
	
	batch = lines[st:end]
	thread = MyProxyChecker(batch, i)
	print("Start -> {0} :: End -> {1} :: Links -> {2}".format(st,end, (end-st)))
	threadsArr.append(thread)
	
for thread in threadsArr:
	thread.start()
	time.sleep(1)

# Wait until done
for thread in threadsArr: thread.join()

print("Done")
