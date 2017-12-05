import numpy as np
import json
from matplotlib import pyplot as plt
from nltk import word_tokenize
from nltk.corpus import stopwords
from shutil import copyfile

def filter_points(i_f, of1, of2):
	g = open(of1, 'w', encoding='utf-8')
	h = open(of2, 'w', encoding='utf-8')
	c1 = 0
	c2 = 0
	with open(i_f, encoding='utf-8') as f:
		for line in f:
			items = line.lower().split(',')
			c1 += 1
			if len(items) == 5:
				g.write(line)
				c2 += 1
			else:
				h.write(line)
	g.close()
	h.close()
	print(c1)
	print(c2)

def get_attributes(i_f):
	attr_dic = {'id': [], 'url': [], 'additional': [], 'breadcrumbs': [], 'label': []}
	#data = []
	with open(i_f, encoding='utf-8') as f:
		for line in f:
			flag = 0
			items = line[0:-1].lower().split(',')
			attr_dic['id'].append(items[0])
			attr_dic['label'].append(items[-1])
			if len(items) == 5:
				attr_dic['url'].append(items[1])
				attr_dic['additional'].append(items[2])
				attr_dic['breadcrumbs'].append(items[3])
				#data.append(line)
			else:
				if len(items[1]) == 0 or items[1][0] != '"':
					flag = 1
					attr_dic['url'].append(items[1])
				elif items[1][0] == '"':
					flag = 2
					item = items[1]
					for i in range(2, len(items)-1):
						item = item + ',' + items[i]
					item = item.replace('"""','"')
					item = item.replace('",','*end_item*')
					item = item.replace(',"','*end_item*')
					item = item.replace('*end_item**end_item*','*end_item*')
					items = item.split('*end_item*')
					#print(items)
					if len(items) == 3:
						attr_dic['url'].append(items[0])
						attr_dic['additional'].append(items[1])
						attr_dic['breadcrumbs'].append(items[2])
						#data.append(line)
					else:
						print('Anomaly: 1')
						print(items)
				if flag == 1:
					if len(items[2]) == 0 or items[2][0] != '"':
						flag = 3
						attr_dic['additional'].append(items[2])
					elif items[2][0] == '"':
						flag = 4
						item = items[2]
						for i in range(3, len(items)-1):
							item = item + ',' + items[i]
						item = item.replace('"""','"')
						item = item.replace('",','*end_item*')
						item = item.replace(',"','*end_item*')
						item = item.replace('*end_item**end_item*','*end_item*')
						items = item.split('*end_item*')
						if len(items) == 2:
							attr_dic['additional'].append(items[0])
							attr_dic['breadcrumbs'].append(items[1])
							#data.append(line)
						else:
							print('Anomaly: 2')
							print(items)
				if flag == 3:
					if len(items[3]) == 0 or items[3][0] != '"':
						flag = 5
						attr_dic['breadcrumbs'].append(items[3])
					elif items[3][0] == '"':
						flag = 6
						item = items[3]
						for i in range(4, len(items)-1):
							item = item + ' ' + items[i]
						item = item.replace('"""','"')
						item = item.replace('",','*end_item*')
						item = item.replace(',"','*end_item*')
						item = item.replace('*end_item**end_item*','*end_item*')
						items = item.split('*end_item*')
						if len(items) == 1:
							attr_dic['breadcrumbs'].append(items[0])
							#data.append(line)
						else:
							print('Anomaly: 3')
				if flag == 0:
					#count += 1
					#print(items)
					#print(len(items))
					print('Anomaly !!!!')
	print('Attibutes obtained !!!!')
	#with open('final_train.txt', 'w', encoding='utf-8') as f:
	#	for d in data:
	#		f.write(d)
	#print(len(data))
	return attr_dic

def write_attr_file(data, name):
	with open(name + '.txt', 'w', encoding='utf-8') as f:
		for d in data:
			f.write(d + '\n')
	print('Write complete for ', name)

def get_class_count(i_f):
	count = {'music': 0, 'rest': 0, 'books': 0, 'videos': 0}
	with open(i_f, encoding='utf-8') as f:
		for line in f:
			count[line[0:-1]] += 1
	plt.bar(range(len(count)), count.values(), align='center')
	plt.xticks(range(len(count)), count.keys())
	plt.savefig('Class_count.png')

def get_additional_attr(if1, if2,):
	label_idx = {'books': [], 'videos': [], 'music': [], 'rest': []}
	count = 0
	with open(if2, encoding='utf-8') as f:
		for line in f:
			label_idx[line[0:-1]].append(count)
			count += 1
	print('Labels read !!!!')

	attr = {'books': {}, 'videos': {}, 'music': {}, 'rest': {}}
	count = 0
	with open(if1, encoding='utf-8') as f:
		for line in f:
			items = line.split(';')
			for i in items:
				j = i.split('=')
				if count in label_idx['books']:
					if j[0] not in attr['books']:
						attr['books'][j[0]] = 1
					else:
						attr['books'][j[0]] += 1
				elif count in label_idx['music']:
					if j[0] not in attr['music']:
						attr['music'][j[0]] = 1
					else:
						attr['music'][j[0]] += 1
				elif count in label_idx['videos']:
					if j[0] not in attr['videos']:
						attr['videos'][j[0]] = 1
					else:
						attr['videos'][j[0]] += 1
				elif count in label_idx['rest']:
					if j[0] not in attr['rest']:
						attr['rest'][j[0]] = 1
					else:
						attr['rest'][j[0]] += 1
			count += 1

	fig = plt.figure()
	plt.bar(range(len(attr['books'])), attr['books'].values(), align='center')
	plt.xticks(range(len(attr['books'])), attr['books'].keys())
	fig.savefig('books_attr_count.png')
	with open('books_features.txt', 'w', encoding='utf-8') as f:
		for k in attr['books'].keys():
			f.write(k + '\n')
	fig = plt.figure()
	plt.bar(range(len(attr['music'])), attr['music'].values(), align='center')
	plt.xticks(range(len(attr['music'])), attr['music'].keys())
	fig.savefig('music_attr_count.png')
	with open('music_features.txt', 'w', encoding='utf-8') as f:
		for k in attr['music'].keys():
			f.write(k + '\n')
	fig = plt.figure()
	plt.bar(range(len(attr['videos'])), attr['videos'].values(), align='center')
	plt.xticks(range(len(attr['videos'])), attr['videos'].keys())
	fig.savefig('videos_attr_count.png')
	with open('videos_features.txt', 'w', encoding='utf-8') as f:
		for k in attr['videos'].keys():
			f.write(k + '\n')
	fig = plt.figure()
	plt.bar(range(len(attr['rest'])), attr['rest'].values(), align='center')
	plt.xticks(range(len(attr['rest'])), attr['rest'].keys())
	fig.savefig('rest_attr_count.png')
	with open('rest_features.txt', 'w', encoding='utf-8') as f:
		for k in attr['rest'].keys():
			f.write(k + '\n')

def filter_breadcrumbs(i_f, o_f):
	symb = ['!', '"', '#', '$', '%', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
	attr = {}
	stop_words = set(stopwords.words('english'))
	g = open(o_f, 'w', encoding='utf-8')
	with open(i_f, 'r', encoding='utf-8') as f:
		for line in f:
			items = word_tokenize(line[0:-1])
			items = [i for i in items if i not in symb]
			items = [i for i in items if not i in stop_words]
			item = []
			for i in items:
				if i != '>' and i != '&':
					if i.isalpha() == True:
						item.append(i)
						if i not in attr:
							attr[i] = 1
						else:
							attr[i] += 1
			items = " ".join(item)
			g.write(items + '\n')
	g.close()
	with open('breadcrumb_features.txt', 'w', encoding='utf-8') as f:
		for k in attr.keys():
			f.write(k + ':' + str(attr[k]) + '\n')

def get_breadcrumb_features(i_f, k):
	attr = {}
	count = 0
	with open(i_f, 'r', encoding='utf-8') as f:
		for line in f:
			line = line[0:-1]
			items = line.split(':')
			if int(items[1]) > k:
				attr[items[0]] = count
				count += 1
	return attr

def get_additional_features(i_f, k):
	attr = {}
	count = 0
	with open(i_f, 'r', encoding='utf-8') as f:
		for line in f:
			line = line[0:-1]
			items = line.split(':')
			if int(items[1]) > k:
				attr[items[0]] = count
				count += 1
	return attr

def get_labels(i_f):
	l = []
	with open(i_f, 'r', encoding='utf-8') as f:
		for line in f:
			if line[0:-1] == 'books':
				l.append([1, 0, 0, 0])
			elif line[0:-1] == 'music':
				l.append([0, 1, 0, 0])
			elif line[0:-1] == 'videos':
				l.append([0, 0, 1, 0])
			elif line[0:-1] == 'rest':
				l.append([0, 0, 0, 1])
	return l

def filter_additional(i_f, o_f):
	symb = ['!', '"', '#', '$', '%', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
	stop_words = set(stopwords.words('english'))
	attr = {}
	g = open(o_f, 'w', encoding='utf-8')
	with open(i_f, 'r', encoding='utf-8') as f:
		for line in f:
			items = line.split(';')
			s = ''
			for i in items:
				j = i.split('=')[0]
				s = s + j + ' '
			items = word_tokenize(s)
			items = [i for i in items if i not in symb]
			items = [i for i in items if not i in stop_words]
			item = []
			for i in items:
				if i.isalpha() == True:
					item.append(i)
					if i not in attr:
						attr[i] = 1
					else:
						attr[i] += 1
			items = " ".join(item)
			g.write(items + '\n')
	g.close()
	with open('additional_features.txt', 'w', encoding='utf-8') as f:
		for k in attr.keys():
			f.write(k + ':' + str(attr[k]) + '\n')

def get_additional_vector(s, attr):
	a = [0 for i in range(len(attr))]
	items = s.split(' ')
	if len(items) > 0:
		for i in items:
			if i in attr:
				a[attr[i]] = 1
	return a

def get_breadcrumb_vector(s, attr):
	a = [0 for i in range(len(attr))]
	items = s.split(' ')
	if len(items) > 0:
		for i in items:
			if i in attr:
				a[attr[i]] += 1
	return a

def prepare_data(if1, if2, attr1, attr2, l):
	data1 = []
	with open(if1, 'r', encoding='utf-8') as f:
		for line in f:
			data1.append(line)
	data2 = []
	with open(if2, 'r', encoding='utf-8') as f:
		for line in f:
			data2.append(line)

	data = []
	labels = []
	k = 0
	for i in range(len(data1)):
		d1 = get_additional_vector(data1[i], attr1)
		d2 = get_breadcrumb_vector(data2[i], attr2)
		d = d1 + d2
		data.append(d)
		labels.append(l[i])
		if len(data) == 10000:
			np.savez_compressed('./instances/' + str(k), data=data, labels=labels)
			k += 1
			data = []
			labels = []
	np.savez_compressed('./instances/' + str(k), data=data, labels=labels)

def prepare_test_data(if1, if2, attr1, attr2, l):
	data1 = []
	with open(if1, 'r', encoding='utf-8') as f:
		for line in f:
			data1.append(line)
	data2 = []
	with open(if2, 'r', encoding='utf-8') as f:
		for line in f:
			data2.append(line)

	data = []
	ids = []
	k = 0
	for i in range(len(data1)):
		d1 = get_additional_vector(data1[i], attr1)
		d2 = get_breadcrumb_vector(data2[i], attr2)
		d = d1 + d2
		data.append(d)
		ids.append(l[i])
		if len(data) == 20000:
			np.savez_compressed('./submission/' + str(k), data=data, ids=ids)
			k += 1
			data = []
			ids = []
	np.savez_compressed('./submission/' + str(k), data=data, ids=ids)

def main():
	i_f = 'train.csv'
	of1 = 'filtered_data.txt'
	of2 = 'unfiltered_data.txt'
	filter_points(i_f, of1, of2)
	#i_f = 'final_train.txt'
	attr = get_attributes(i_f)
	write_attr_file(attr['url'], 'url')
	write_attr_file(attr['additional'], 'additional')
	write_attr_file(attr['breadcrumbs'], 'breadcrumbs')
	write_attr_file(attr['label'], 'label')
	#analyse_additional(i_f)
	get_class_count('label.txt')
	get_additional_attr('additional.txt', 'label.txt')
	i_f = 'breadcrumbs.txt'
	o_f = 'filtered_breadcrumbs.txt'
	filter_breadcrumbs(i_f, o_f)
	i_f = 'additional.txt'
	o_f = 'filtered_additional.txt'
	filter_additional(i_f, o_f)

	i_f = 'label.txt'
	labels = get_labels(i_f)
	np.savez('Labels', labels=labels)
	i_f = 'breadcrumb_features.txt'
	breadcrumb_feat = get_breadcrumb_features(i_f, 100)
	np.savez('breadcrumb_feat', feat=breadcrumb_feat)
	print(len(breadcrumb_feat))
	i_f = 'additional_features.txt'
	additional_feat = get_additional_features(i_f, 10)
	np.savez('additional_feat', feat=additional_feat)
	print(len(additional_feat))

	if1 = 'filtered_additional.txt'
	if2 = 'filtered_breadcrumbs.txt'
	prepare_data(if1, if2, additional_feat, breadcrumb_feat, labels)
	for i in range(7):
		perm = np.random.permutation(61)
		for p in perm[0:50]:
			copyfile('instances/' + str(p) + '.npz', 'instances/' + str(i) + '/train/' + str(p) + '.npz')
		for p in perm[50:]:
			copyfile('instances/' + str(p) + '.npz', 'instances/' + str(i) + '/test/' + str(p) + '.npz')

	i_f = 'evaluation.csv'
	attr = get_attributes(i_f)
	write_attr_file(attr['additional'], 'additional_eval')
	write_attr_file(attr['breadcrumbs'], 'breadcrumbs_eval')
	write_attr_file(attr['label'], 'id_eval')
	i_f = 'breadcrumbs_eval.txt'
	o_f = 'filtered_breadcrumbs_eval.txt'
	filter_breadcrumbs(i_f, o_f)
	i_f = 'additional_eval.txt'
	o_f = 'filtered_additional_eval.txt'
	filter_additional(i_f, o_f)

	i_f = 'id_eval.txt'
	labels = []
	with open(i_f, 'r', encoding='utf-8') as f:
		for line in f:
			labels.append(line[0:-1])
	d = np.load('breadcrumb_feat.npz')
	breadcrumb_feat = d['feat'].item()
	d = np.load('additional_feat.npz')
	additional_feat = d['feat'].item()
	if1 = 'filtered_additional_eval.txt'
	if2 = 'filtered_breadcrumbs_eval.txt'
	prepare_data(if1, if2, additional_feat, breadcrumb_feat, labels)

if __name__ == '__main__':
	main()
