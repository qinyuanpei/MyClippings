import os
import hashlib

INPUT_DIR = './data/微信读书/'
OUTPUT_DIR = './docs/books/'

def mkdocs(fileName):
    with open(fileName,'rt',encoding='utf-8') as fi:
        texts = fi.readlines()
        bookName = texts[0].replace('\n','')
        bookAuthor = texts[1].replace('\n','')
        bookTitle = '{0}({1})'.format(bookName,bookAuthor)
        bookId = hashlib.md5(bookTitle.encode(encoding='utf-8')).hexdigest()
        bookPath = os.path.join(OUTPUT_DIR, u"%s.md" % bookId)
        with open(bookPath,'wt',encoding='utf-8') as fo:
            fo.write('# ' + bookTitle + "\n\n")
            content = ''.join(texts[3:]).replace('>>','>').replace('\u25c6','##')
            fo.write(content)

def main():
    files = os.listdir(INPUT_DIR)
    if len(files) > 0:
        for file in files:
            fileName = os.path.join(INPUT_DIR, file)
            mkdocs(fileName)
        
if __name__ == '__main__':
   main()