import pickle
import os

my_path = os.path.dirname(os.path.abspath(__file__))

def hex2bytes(hex_string):
	return bytes([int(hex_string[:2], 16), int(hex_string[2:], 16)])

def hex2unicode(hex_string):
	return chr(int(hex_string, 16))

def load_u2b_from_txt():
	result = {}
	with open(my_path+'/uao250-u2b.txt','r',encoding='utf-8') as f:
		for line in f.read().strip().splitlines():
			if line[0] == '#':
				continue
			big, uni = line.strip().split(' ')
			result[hex2unicode(uni[2:])] = hex2bytes(big[2:])
	return result

def load_b2u_from_txt():
	result = {}
	with open(my_path+'/uao250-b2u.txt','r',encoding='utf-8') as f:
		for line in f.read().strip().splitlines():
			if line[0] == '#':
				continue
			big, uni = line.strip().split(' ')
			result[hex2bytes(big[2:])] = hex2unicode(uni[2:])
	return result


try:
	u2b_map = pickle.load(open(my_path+'/uao250-u2b.pickle','rb'))
except:
	u2b_map = load_u2b_from_txt()
	pickle.dump(u2b_map, open(my_path+'/uao250-u2b.pickle','wb'))

try:
	b2u_map = pickle.load(open(my_path+'/uao250-b2u.pickle','rb'))
except:
	b2u_map = load_b2u_from_txt()
	pickle.dump(b2u_map, open(my_path+'/uao250-b2u.pickle','wb'))
			
def encode(unicode_string):
	ans = b''
	for u in unicode_string:
		try:
			ans += u2b_map[u]
		except:
			ans += u.encode('cp950')
	return ans

def decode(byte_string):
	ans = u''
	i = 0
	while i < len(byte_string):
		b = byte_string[i:i+2]
		try:
			ans += b2u_map[b]
			i +=2
		except:
			ans += byte_string[i].decode('cp950')
			i +=1
	return ans
				