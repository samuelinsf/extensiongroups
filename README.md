# extensiongroups
report size of and filesystem cache use of solar / lucene indexes by file extension

Example use:

    $ extension_groups.py solr-data/index
    extn                 size        running total        % in fs cache
    gen                   20                   20                100.0
    fnm            1_689_186            1_689_206                100.0
    del            1_814_258            3_503_464                100.0
    tii           26_622_930           30_126_394                 14.1
    fdx          124_092_928          154_219_322                 99.9
    tis        2_223_265_645        2_377_484_967                 47.1
    prx        5_906_162_797        8_283_647_764                  8.1
    frq        6_382_376_619       14_666_024_383                 23.3
    fdt       12_435_537_372       27_101_561_755                  5.6
    nrm       84_786_480_823      111_888_042_578                  0.8


A description of the file extensions can be found [here](http://lucene.apache.org/core/4_10_3/core/org/apache/lucene/codecs/lucene410/package-summary.html#file-names).
