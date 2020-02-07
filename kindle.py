#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import json
import os
import re
import uuid
import hashlib

BOUNDARY = u"==========\r\n"
DATA_FILE = u"clips.json"
OUTPUT_DIR = u"./docs/books"


def get_sections(filename):
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    content = content.replace(u'\ufeff', u'')
    return content.split(BOUNDARY)


def get_clip(section):
    clip = {}

    lines = [l for l in section.split(u'\r\n') if l]
    if len(lines) != 3:
        return

    clip['book'] = lines[0]
    clip['remark'] = lines[1][1:].strip()
    match = re.search(r'(\d+)-\d+', lines[1])
    if not match:
        return
    position = match.group(0)

    clip['position'] = '#' + position
    clip['content'] = lines[2]

    match = re.search(r'(\d+)-\d+', lines[1])
    if not match:
        return

    return clip


def export_txt(clips):
    """
    Export each book's clips to single text.
    """
    if(not os.path.exists(OUTPUT_DIR)):
        os.makedirs(OUTPUT_DIR) 

    books = []
    # Generate books/book.md
    for book in clips:
        lines = []
        for pos in sorted(clips[book]):
            lines.append(clips[book][pos][0])
            lines.append('>' + clips[book][pos][1])
        
        book = book.replace('wheremylife','WhereMyLife')
        fileId = hashlib.md5(book.encode(encoding='utf-8')).hexdigest()
        fileName = os.path.join(OUTPUT_DIR, u"%s.md" % fileId)
        books.append({"bookName":book,"fileId":fileId})
        with open(fileName, 'w', encoding='utf-8') as f:
            f.write('# {book}\n\n'.format(book=book))
            f.write("\n\n".join(lines))

    # Generate _sidebar.md
    books = list(map(lambda x:"* [{bookName}](books/{fileId}.md)".format(bookName=x["bookName"],fileId=x["fileId"]), books))
    with open('./docs/_sidebar.md', 'w', encoding='utf-8') as f:
        f.write("* [首页](/)\n\n")
        f.write("\n\n".join(books))


def load_clips():
    """
    Load previous clips from DATA_FILE
    """
    try:
        with open(DATA_FILE, 'rb') as f:
            return json.load(f)
    except (IOError, ValueError):
        return {}


def save_clips(clips):
    """
    Save new clips to DATA_FILE
    """
    with open(DATA_FILE, 'wb') as f:
        json.dump(clips, f)


def main():
    # load old clips
    clips = collections.defaultdict(dict)
    clips.update(load_clips())

    # extract clips
    sections = get_sections(u'My Clippings.txt')
    for section in sections:
        clip = get_clip(section)
        if clip:
            clips[clip['book']][str(clip['position'])] = (clip['remark'],clip['content'])

    # remove key with empty value
    clips = {k: v for k, v in clips.items() if v}

    # save/export clips
    # save_clips(clips)
    export_txt(clips)


if __name__ == '__main__':
    main()
