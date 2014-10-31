# Just an example of basic signals

from blinker import signal
send_data = signal('send-data')
@send_data.connect
def receive_data(sender, **kw):
	print("Caught signal from %r, data %r" % (sender, kw))
	return 'received!'

result=send_data.send('anony',abc=123)
