#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Programma scemo & idiota per convertire i file di testo di windows (usualmente codificati in cp1252) in utf8
# 2008-11-23 - Versione iniziale

if __name__ == '__main__':
	from sys import argv, stdin, stdout, stderr, exit
	if len(argv) not in (1, 2, 3) or '--help' in argv or '-h' in argv:
		stderr.write("USO: %s [INFILE [OUTFILE]]\n" % argv[0])
		exit(-1)
	try:
		infile = open(argv[1], "r")
	except IndexError:
		infile = stdin
	try:
		outfile = open(argv[2], "w")
	except IndexError:
		outfile = stdout
	outfile.writelines([row.replace('\r','').decode('cp1252').encode('utf8') for row in infile.readlines()])
	infile.close()
	outfile.close()

