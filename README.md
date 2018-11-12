# WGDI

[![Latest PyPI version](https://img.shields.io/pypi/v/wgdi.svg)](https://pypi.python.org/pypi/wgdi)

| | |
| --- | --- |
| Author  | Pengchuan Sun ([sunpengchuan](https//github.com/sunpengchuan)) |
| Email   | <sunpengchuan@gmail.com> |
| License | [BSD](http://creativecommons.org/licenses/BSD/) |

## Description

Finely identify the whole genome duplication events and generate the genomic homology tables.

## Features

-   Generate homologous gene dotplots .
-   Generate the genomic homology table through the blocks by colinearscan and mcscanx.
-   Calculate Ks of homologous pairs.
-   Mark Ks value of homologous blocks in homologous gene dotplots to assist in determining collinear fragments produced by different doubling events.

## Installation

-   [python3](https://www.python.org/)
-   [pandas](https://pandas.pydata.org/)
-   [biopython](http://www.biopython.org/)
-   [paml](http://web.mit.edu/6.891/www/lab/paml.html)
-   [pal2nal](http://www.bork.embl.de/pal2nal/)

```bash
pip install wgdi
```

## Usage

Here are two ways to use this module. The first one is to pass in a configuration parameter options through a module call. See options for specific parameters. The second is to execute the script and write configuration parameters options to the configuration file whose extension name is. conf. See options for specific execution methods.

## Options


```bash

$ wgdi -h

  -d DOTPLOT, --dotplot DOTPLOT
                        More information, try to use 'wgdi -d example'
  -c CORRESPONDENCE, --correspondence CORRESPONDENCE
                        More information, try to use 'wgdi -c example'
  -a ALIGNMENT, --alignment ALIGNMENT
                        More information, try to use 'wgdi -a example'
  -r RETAIN, --retain RETAIN
                        More information, try to use 'wgdi -r example'
  -bk BLKKS, --blkks BLKKS
                        More information, try to use 'wgdi -bk example'
  -ks CALKS, --calks CALKS
                        More information, try to use 'wgdi -ks example'

```

Each parameter is a handler, and the details can be obtained through wgdi -* example (* represent argument) and save to `your `.conf or options.

```
$ wgdi -d example

    [dotplot]
    blast = blast file
    gff1 =  gff1 file
    gff2 =  gff2 file
    lens1 = lens1 file
    lens2 = lens2 file
    genome1_name =  Genome1 name
    genome2_name =  Genome2 name
    WGD = 1
    markersize = 0.5
    savefile = savefile(.png,.pdf)
```
After modifying the parameters, execute   `class`. run () or wgdi -*  `your` .conf .

```python
from wgdi.dotplot import dotplot
options = {'blast': 'os_os.1e-5.blast',
           'gff1': 'os.gff',
           'gff2': 'os.gff',
           'lens1': 'os_chrs.lens',
           'lens2': 'os_chrs.lens',
           'genome1_name': 'os',
           'genome2_name': 'os',
           'WGD ': 1,
           'markersize': 0.5,
           'savefile': 'os_os.dotplot.new.png'
           }
options = list(options.items())
newdot = dotplot(options)
newdot.run()
```