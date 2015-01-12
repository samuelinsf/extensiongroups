#!/usr/bin/env python
#
# Offered under GNU GENERAL PUBLIC LICENSE Version 2, June 1991
# Written by github.com/samuelinsf 2014
#
# This tool sums up the sizes of files in a
# directory grouping by extension.
#
# It produces sorted output by extension group size,
# intended to help an operator understand the ram
# requirements of a lucene index.
#
# A guide to what each extension type contains:
# http://lucene.apache.org/core/4_10_3/core/org/apache/lucene/codecs/lucene410/package-summary.html#file-names
#
# These only come out if you are not using the compact index file format.
# (solr defaults to not using the compact index format)
# https://cwiki.apache.org/confluence/display/solr/IndexConfig+in+SolrConfig#IndexConfiginSolrConfig-UseCompoundFile
#

import ctypes
import mmap
import optparse
import os
import os.path
import re
import resource
import sys


def incore_pages(filename):
    # int mincore(void *addr, size_t length, unsigned char *vec);
    # len of vec:  (length+PAGE_SIZE-1) / PAGE_SIZE
    pagesize = resource.getpagesize()
    
    f = open(filename, 'r+b')
    mm = mmap.mmap(f.fileno(), 0)
    vec_len = (len(mm) + pagesize - 1)/pagesize
    vec = ctypes.create_string_buffer(vec_len)

    libc = ctypes.cdll.LoadLibrary("libc.so.6")
    b = ctypes.c_void_p.from_buffer(mm)
    r = ctypes.byref(b)
    libc.mincore(r, len(mm), vec)

    incore = 0
    notincore = 0
    for v in vec:
        if (ord(v) & 1):
            incore += 1
        else:
            notincore += 1
    return(incore, notincore)


def add_underscores(n):
    n = str(n)
    running = 1
    while running:
        (n, running) = re.subn('^(\d+)(\d\d\d)', r'\1_\2', n)
    return n


def report(directory):
    extensions = {}
    incore = {}
    notincore = {}

    for p in os.listdir(directory):
        if os.path.isfile(p) and '.' in p:
            s = os.stat(p)
            e = p.rsplit('.',1)[1]
            sum = s.st_size + extensions.get(e, 0)
            if s.st_size < 1:
                continue
            (i, noti) = incore_pages(p)
            extensions[e] = sum
            incore[e] = i + incore.get(e,0)
            notincore[e] = noti + notincore.get(e,0)

    total=0
    print "%s %20s %20s %20s" %('extn', 'size', 'running total', '% in fs cache')
    for extension in sorted(extensions, key = lambda x : extensions[x]):
        size = extensions[extension]
        total += size
        print "%s %20s %20s %20.1f" %(extension, add_underscores(size), add_underscores(total), 100*(float(incore[extension])/ (incore[extension] + notincore[extension])))


def main():
    usage = "usage: %prog [options] [directory_to_analyze]"
    parser = optparse.OptionParser(usage)
    (options, args) = parser.parse_args()
    directory = '.'
    if len(args) == 1:
        directory = args[0]
    if len(args) > 1:
        parser.print_help()
        exit(1)
    report(directory)

if '__main__' == __name__:
    main()

