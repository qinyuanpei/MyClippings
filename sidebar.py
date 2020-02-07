import os
import hashlib

INPUT_DIR = './docs/books/'

def main():
    files = os.listdir(INPUT_DIR)
    if len(files) > 0:
        with open('./docs/_sidebar.md','wt', encoding='utf-8') as fo:
            fo.write('* [首页](/)\n\n')
            for file in files:
                fileName = os.path.join(INPUT_DIR, file)
                with open(fileName,'rt', encoding='utf-8') as fi:
                    bookTitle = fi.readlines()[0].replace('#','').strip()
                    bookLink = 'books/' + file
                    bookNav = '* [{0}]({1})\n\n'.format(bookTitle, bookLink)
                    fo.write(bookNav)
                
if __name__ == '__main__':
   main()