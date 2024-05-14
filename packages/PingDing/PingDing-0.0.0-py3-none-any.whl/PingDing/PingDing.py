import subprocess
import threading
import time
import tkinter

def getTimeS():
	return time.time()

def pingReader(p, out):
	for line in iter(p.stdout.readline, b''):
		mline = str(line)
		out['msg'] = mline
		i_time = mline.find('time')
		if i_time >= 0:
			out['tUpdate'] = getTimeS()
			out['rtt']     = mline[(i_time+5):(i_time+9)]

class Node:
	def __init__(self, addr):
		self.p = subprocess.Popen(['ping', '-n', addr], stdout=subprocess.PIPE)
		self.out = { 
			'tUpdate': getTimeS(), 
			'rtt'    : float('nan'),
			'msg'    : 'Init'
		}
		self.t = threading.Thread(target=pingReader, args=(self.p, self.out))
		self.t.start()

	def getStatus(self):
		return {
			'rtt':  float(self.out['rtt']),
			'tAge': getTimeS() - self.out['tUpdate'],
			'lastMsg': self.out['msg']
		}

	def __del__(self):
		self.p.kill()

class PingLabel:
	def __init__(self, window, tMax, row, addr):
		self.tMax = tMax
		self.lbl = tkinter.Label(window, text=addr)
		self.lbl.grid(column=0,row=row)
		self.node = Node(addr)
		self.updateColor(window)

	def updateColor(self, window):
		colorVal = int(max(min(self.node.getStatus()['tAge'] / self.tMax, 1), 0) * 255)
		self.lbl.config(bg="#%02X%02X%02X" % (colorVal, 255 - colorVal, 0))

		window.after(500, self.updateColor, window)


def constructMainWindow(tMax, addrs):
	window = tkinter.Tk()
	window.title('PingDing')

	irow = 0
	for addr in addrs:
		PingLabel(window, tMax, irow, addr)
		irow = irow + 1

	window.protocol('WM_DELETE_WINDOW', lambda : window.destroy())
	window.mainloop()


