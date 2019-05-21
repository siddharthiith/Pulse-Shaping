# error vs number of bits for various snrs

import numpy as np 
import matplotlib.pyplot as plt 
import scipy

alpha =0.35

t = np.linspace(-4,4,65)

p = [0]*65

for i in range(0,65):
	if t[i]==0:
		p[i] = (1-alpha)+4*alpha/np.pi
	elif t[i] == 1/(4*alpha):
		p[i] = (alpha/(np.sqrt(2)))*((1+2/np.pi)*np.sin(np.pi/(4*alpha))+ (1-2/np.pi)*np.cos(np.pi/(4*alpha)))
	elif t[i] == -1/(4*alpha):
		p[i] = (alpha/(np.sqrt(2)))*((1+2/np.pi)*np.sin(np.pi/(4*alpha))+ (1-2/np.pi)*np.cos(np.pi/(4*alpha)))
	else:
		p[i] = (np.sin(np.pi*t[i]*(1-alpha))+ 4*alpha*t[i]*np.cos(np.pi*t[i]*(1+alpha)))/(np.pi*t[i]*(1-(4*alpha*t[i])**2))

def ber(numbits,snrdb):
	num_bits = int(numbits)
	bits = 2*np.random.randint(2, size = num_bits)-1
	os = 8
	bits_os = []
	for i in range(0,num_bits):
		bits_os.append(bits[i])
		for j in range(0,os-1):
			bits_os.append(0)
	output_of_srrc_filterr = np.convolve(bits_os, p)
	noise = np.random.normal(0,np.sqrt(10**(-snrdb*0.1)),len(output_of_srrc_filterr))
	for i in range(0,len(output_of_srrc_filterr)):
		output_of_srrc_filterr[i] = output_of_srrc_filterr[i]+noise[i]
	y = np.convolve(output_of_srrc_filterr,p)
	y_truncated = y[65-1:len(y)]
	y_down = []
	for i in range(0,num_bits):
		y_down.append(y_truncated[0+8*i])
	#bits_hat = []
	difference = 0
	for i in range(0, num_bits):
		if (y_down[i]>0 and bits[i]==0 ) or (y_down[i]<0 and bits[i]==1 ) :
			difference = difference+1
	print "bits="+str(num_bits)+"	snrdb="+str(snrdb)+"	difference="+str(difference)
	return difference
		
snrdb = np.linspace(1,5,5)
num_bits = np.linspace(100,int(1e5),10)
vecber = scipy.vectorize(ber)

for j in range(0,5):
	plt.plot(num_bits,vecber( num_bits , snrdb[j] ),label=str(snrdb[j]))
	
plt.legend(loc='best')
plt.grid()
plt.show()

#plt.plot(output_of_srrc_filterr,'r--')
#plt.plot(y,'r--')
# plt.plot(y_down,'o')
#plt.grid()
#plt.show()
