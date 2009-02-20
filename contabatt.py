#!/usr/bin/env python
# -*- encoding: utf-8 -*-

def main(stream, encoding):
    """Conta le battute di uno stream usando il layout della tastiera italiana
mgs  as  mds  is   id  mdd  ad  mgd
-----------------------------------
\12   3   4   56   78   9   0   'ì
 q   w   e   rt   yu   i   o   pè+
  a   s   d   fg   hj   k   l   òàù
 < z   x   c   vb   nm   ,   .   - """
    d = { 'sinistra': {('\\12qa<z', 'mignolo'): 0, ('3wsx', 'anulare'): 0,
                    ('4edc', 'medio'): 0,  ('56rtfgvb', 'indice'): 0},
            'destra': {('78yuhjnm', 'indice'): 0, ('9ik,', 'medio'): 0,
                    ('0ol.', 'anulare'): 0, (u"'ìpè+òàù-", 'mignolo'): 0} }
    tot = 0
    for row in stream:
        for char in row.decode(encoding):
            for hand in d:
                for (char_set, finger) in d[hand]:
                    if char in char_set:
                        d[hand][(char_set, finger)] += 1
                        tot += 1
                        break
    print "Totale battute: %d" % tot
    for hand in 'sinistra', 'destra':
        tot_hand = sum(d[hand][key] for key in d[hand])
        print "\tMano %s: %d (%5.2f%%)" % (hand, tot_hand, tot_hand*100./tot)
        for finger in 'indice', 'medio', 'anulare', 'mignolo':
            tot_finger = d[hand][filter(lambda k: k[1] == finger, d[hand])[0]]
            print "\t\t%s: %d\t(%5.2f%% mano\t%5.2f%% tot)" % (finger,
                    tot_finger, tot_finger*100./tot_hand, tot_finger*100./tot)

if __name__ == '__main__':
    from sys import argv, stdin
    if len(argv) > 1:
        stream = open(argv[1])
    else:
        stream = stdin
    if len(argv) > 2:
        encoding = argv[2]
    else:
        encoding = 'utf-8'
    main(stream, encoding)
