#!/usr/bin/env python3
import sys
import gzip
import json
import argparse
sys.path.append('.')
from scripts.data_convert.text_proc import *
from scripts.data_convert.convert_common import *

parser = argparse.ArgumentParser(description='Convert MSMARCO-adhoc documents.')
parser.add_argument('--input', metavar='input file', help='input file',
                    type=str, required=True)
parser.add_argument('--output', metavar='output file', help='output file',
                    type=str, required=True)
parser.add_argument('--max_doc_size', metavar='max doc size bytes', help='the threshold for the document size, if a document is larger it is truncated',
                    type=int, default=MAX_DOC_SIZE)


args = parser.parse_args()
print(args)

inpFile = FileWrapper(args.input)
outFile = FileWrapper(args.output, 'w')
maxDocSize = args.max_doc_size

stopWords = readStopWords(STOPWORD_FILE, lowerCase=True)
print(stopWords)
nlp = SpacyTextParser("en_core_web_sm", stopWords, keepOnlyAlphaNum=True)

# Input file is a TSV file
ln=0
for line in inpFile:
  ln+=1
  if not line: 
    continue
  line = line[:maxDocSize] # cut documents that are too long!
  fields = line.split('\t')
  if len(fields) != 4:
    print('Misformated line %d ignoring:' % ln)
    print(line.replace('\t', '<field delimiter>'))
    continue

  did, url, title, body = fields

  title_lemmas, title_unlemm = nlp.procText(title)
  body_lemmas, body_unlemm = nlp.procText(body)

  title_lemmas = title_lemmas.lower()
  title_unlemm = title_unlemm.lower()
  body_lemmas = body_lemmas.lower()
  body_unlemm = body_unlemm.lower()

  text = title_lemmas + ' ' + body_lemmas
  text = text.strip()
  doc = {'DOCNO' : did, 'text' : text, 'title' : title_unlemm, 'body' : body_unlemm}
  docStr = json.dumps(doc) + '\n'
  outFile.write(docStr)
  if ln % REPORT_QTY == 0:
    print('Processed %d docs' % ln)

print('Processed %d docs' % ln)

inpFile.close()
outFile.close()