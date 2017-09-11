
from email.parser import Parser
from email_reply_parser import EmailReplyParser
from rake_nltk import Rake
from os import listdir
from os.path import isfile, join
import sys
import nltk
import six
import re
import operator
import io
import os
import talon
import string
import nltk.data
from talon import quotations
from talon.signature.bruteforce import extract_signature
talon.init()


root_path = '../skillmatch/maildir'
mentor_dirs = [join(root_path, f) for f in listdir(root_path) if not isfile(join(root_path, f))]
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

email_ids = set()
table = string.maketrans("","")
corpus = open('corpus.txt', 'w')
for mentor_path in mentor_dirs:
	print mentor_path
	mentor = mentor_path.split('/')[1]
	folders = [join(mentor_path, f) for f in listdir(mentor_path) if not isfile(join(mentor_path, f))]
	text = ''

	for folder in folders:
		mail_files = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
		for mail_file in mail_files:
			with open(mail_file, "r") as f:
				data = f.read()
				email = Parser().parsestr(data)
				email_id = email['Message-ID']
				if email_id not in email_ids:
					email_ids.add(email_id)
					pl = email.get_payload()
					message = EmailReplyParser.parse_reply(pl)
					message, signature = extract_signature(quotations.extract_from_plain(message))
					message = message.lower()

					message = re.sub(r'https?:\/\/.*[\r\n]*', '', message, flags=re.MULTILINE)
					message = message.replace('=', ' ')
					sentences = sent_detector.tokenize(message)
					for s in sentences:
						words = nltk.word_tokenize(s)
						for w in words:
							if re.search('[a-z]', w):
								corpus.write(w.strip() + ' ')					
						corpus.write('\n')
	


