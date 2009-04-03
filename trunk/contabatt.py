#!/usr/bin/env python

def main(stream, encoding):
    d = { 'sinistra': {('\\12qa<z', 'mignolo'): 0, ('3wsx', 'anulare'): 0,
                    ('4edc', 'medio'): 0,  ('56rtfgvb', 'indice'): 0},
            'destra': {('78yuhjnm', 'indice'): 0, ('9ik,', 'medio'): 0,
                    ('0ol.', 'anulare'): 0, ("'\xc3\xacp\xc3\xa8+\xc3\xb2\xc3"
                            "\xa0\xc3\xb9-".decode('utf8'), 'mignolo'): 0} }
    d2 = dict((char, 0) for char in ''.join([e[0] for e in d['sinistra']] +
            [e[0] for e in d['destra']]))
    tot = 0
    for row in stream:
        for char in row.decode(encoding):
            if char in d2:
                d2[char] += 1
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
    print "Divisione per tasto:"
    for char, num in sorted(d2.items(), key=lambda e:e[1], reverse=True):
        if num:
            print "\t%s: %d (%5.2f%%)" % (char, num, num*100./tot)
        else:
            print '\taltri: 0 (0.00%)'
            break # non ne vale la pena

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
