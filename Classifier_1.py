from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

n = 2236
print('Build model...')
model = Sequential()
model.add(Dense(128, input_dim=n, init='uniform', activation='relu'))
model.add(Dense(4, activation='softmax'))
model.compile(loss='binary_crossentropy', optimizer='adam')
model.save_weights('models/initialise')
'''
print("Training...")
batch_size = 64
class_weight = {0:2,1:2,2:2,3:1}
accuracy = []
for m in range(5):
	model.load_weights('models/initialise')
	folder_name = 'instances/' + str(m) + '/train/'
	files = []
	for f in os.listdir(folder_name):
		files.append(folder_name + f)
	for f in files:
		d = np.load(f)
		X = d['data']
		Y = d['labels']
		loss = 0.0
		for p in range(200):
			perm2 = np.random.permutation(len(Y))
			idx = perm2[0:batch_size]
			x = X[idx, :]
			y = Y[idx, :]
			l = model.train_on_batch(x, y, class_weight=class_weight)
			loss += l
		print('Model: ' + str(m) + ' Loss: ' + str(loss))
	model.save_weights('models/' + str(m), overwrite=True)
	print('Training complete for model ', m)

	print("Validating...")
	pred = []
	real = []
	folder_name = 'instances/' + str(m) + '/test/'
	files = []
	for f in os.listdir(folder_name):
		files.append(folder_name + f)
	for f in files:
		d = np.load(f)
		X = d['data']
		Y = d['labels']
		prba = model.predict_proba(X)
		cls = np.argmax(prba, axis=1)
		for c in cls:
			pred.append(c)
		cls = np.argmax(Y, axis=1)
		for c in cls:
			real.append(c)
	with open('models/predictions_' + str(m), 'w') as f:
		for p in pred:
			f.write(str(p) + '\n')
	acc = 0
	for i in range(len(pred)):
		if pred[i] == real[i]:
			acc += 1
	acc = acc / len(pred)
	print('Accuracy: ' + str(acc))
	accuracy.append(acc)
print(accuracy)
'''
print("Submission...")
pred = []
real = []
m = 4
folder_name = './submission/'
files = []
model.load_weights('models/' + str(m))
for f in os.listdir(folder_name):
	files.append(folder_name + f)
for f in files:
	d = np.load(f)
	X = d['data']
	Y = d['labels']
	prba = model.predict_proba(X)
	cls = np.argmax(prba, axis=1)
	for c in cls:
		if c == 0:
			pred.append('books')
		elif c == 1:
			pred.append('music')
		elif c == 2:
			pred.append('videos')
		elif c == 3:
			pred.append('rest')
	for c in Y:
		real.append(c)
with open('models/submissions_model_' + str(m) + '.csv', 'w') as f:
	for i in range(len(pred)):
		f.write(real[i] + ',' + pred[i] + '\n')
