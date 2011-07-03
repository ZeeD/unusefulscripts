# -*- coding: utf-8 -*-

distance = 400  # distance è una distanza in km

def howMuchTime(speed, distance):
    '''speed = distance/time; therefore time = distance/speed'''
    from datetime import timedelta

    td = timedelta(hours=float(distance)/float(speed))
    return timedelta(seconds=td.seconds)

print 'a coprire %dkm' % (distance, )
for speed1 in range(90, 120, 10): # speed è una velocità in km/h
    time1 = howMuchTime(speed1, distance)
    print '\t@%dkm/h ci metto %s' % (speed1, time1)
    for deltas in range(10, 30, 10):   # delta è una differenza di velocità in km/h
        speed2 = speed1 + deltas
        time2 = howMuchTime(speed2, distance)
        deltat = time1 - time2
        print '\t\taccelerando di %dkm/h ci metto %s (e risparmio %s)' % (deltas, time2, deltat)
