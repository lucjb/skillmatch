
from email.parser import Parser
from email_reply_parser import EmailReplyParser
from os import listdir
from os.path import isfile, join
import sys
import numpy as np
import six

import operator
import io
import os
import talon
import re
import nltk

from talon import quotations
from talon.signature.bruteforce import extract_signature
from nltk.corpus import stopwords
talon.init()


sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

root_path = '../skillmatch/maildir'
mentor_dirs = [join(root_path, f) for f in listdir(root_path) if not isfile(join(root_path, f))]

email2mentor = {}
for mentor_path in mentor_dirs:
	folders = [join(mentor_path, f) for f in listdir(mentor_path) if not isfile(join(mentor_path, f))]
	mentor_email_address=None
	for folder in folders:
		if folder.endswith('sent') or folder.endswith('sent_items') or folder.endswith('sent_mail'):
			with open(join(folder, '1.'), "r") as f:
				data = f.read()
				email = Parser().parsestr(data)
				mentor_email_address = email['from']
				email2mentor[mentor_email_address] = mentor_path

c=0
mentor2text = {}
email_ids = set()
for mentor_path in mentor_dirs:
	folders = [join(mentor_path, f) for f in listdir(mentor_path) if not isfile(join(mentor_path, f))]
	for folder in folders:
		mail_files = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
		for mail_file in mail_files:
			with open(mail_file, "r") as f:
				data = f.read()
				email = Parser().parsestr(data)
				email_id = email['Message-ID']
				if email_id in email_ids:
					continue
				email_ids.add(email_id)
				sender = email['from']
				if sender in email2mentor:
					mentor = email2mentor[sender]
					try:
						mentor2text[mentor].append(email)
					except KeyError:
						mentor2text[mentor] = [email]
					c+=1
					if c % 1000==0:
						print c
						
											
print len(email_ids)


word2vec = {}
embeddings = open('word_embeddings.csv')
_, dim = embeddings.next().split()
dim = int(dim)
for line in embeddings:
	wordvec = line.split()
	word = wordvec[0]
	vec = np.array(map(float, wordvec[1:]))
	word2vec[word]=vec

profiles_file = open('profiles.csv', 'w')						
for mentor, emails in mentor2text.iteritems():
	print mentor, len(emails)
	mentor_vec = np.zeros(dim)
	for email in emails:
		pl = email.get_payload()
		message = EmailReplyParser.parse_reply(pl)
		message, signature = extract_signature(quotations.extract_from_plain(message))
		message = message.lower()

		message = re.sub(r'https?:\/\/.*[\r\n]*', '', message, flags=re.MULTILINE)
		message = message.replace('=', ' ')
		sentences = sent_detector.tokenize(message)
		for s in sentences:
			words = nltk.word_tokenize(s)
			words = [word for word in words if word not in stopwords.words('english')]
			for w in words:
				if re.search('[a-z]', w):
					try:
						mentor_vec +=word2vec[w]
					except KeyError:
						pass

	profiles_file.write(mentor.split('/')[-1] + ' ')
	mentor_vec.tofile(profiles_file, sep=' ')
	profiles_file.write('\n')

	

