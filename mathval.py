#!/usr/bin/env python

# piccolo valutatore di funzioni algebriche a 2 parametri
# funzioni supportate: +, -, *, /, ^, (, ), '' (stringa vuota)
# tipo di dati: float
# Q1 = "f(x,y) = "
# Q2 = "[x0:x1:passo] = "
# Q3 = "[y0:y1:passo] = "
# ho in input cose come "3x^2 + 4y + 2 - xy"
# do in output una funzione lambda

def expr(input_string, i=0):
    input_string, i = term(input_string, i)
    if i < len(input_string) and input_string[i] in '+-':
        input_string, i = term(input_string, i+1)
    return input_string, i

def term(input_string, i=0):
    input_string, i = expterm(input_string, i)
    if i < len(input_string) and input_string[i] in '*/':
        input_string, i = expterm(input_string, i+1)
    return input_string, i

def expterm(input_string, i=0):
    input_string, i = factor(input_string, i)
    if i < len(input_string) and input_string[i] == '^':
        input_string, i = factor(input_string, i+1)
    return input_string, i

def factor(input_string, i=0):
    try:
        c = input_string[i]
    except IndexError:
        raise Exception('factor:%s:%d' % (input_string, i))
    if c == '(':
        input_string, i = expr(input_string, i+1)
        try:
            c = input_string[i]
        except IndexError:
            raise Exception('factor:%s:%d' % (input_string, i))
        else:
            if input_string[i] != ')':
                raise Exception('factor:%s:%d' % (input_string, i))
            return input_string, i+1
    elif c in '+-':
        i += 1
    try:
        input_string, i = number(input_string, i)
    except:
        try:
            input_string, i = constant(input_string, i)
        except:
            raise Exception('factor:%s:%d' % (input_string, i))
    return input_string, i

def number(input_string, i=0):
    dotted = False
    try:
        buffer = [ input_string[i] ]
    except IndexError:
        raise Exception('number:%s:%d' % (input_string, i))
    else:
        if buffer[0] not in '0123456789.':
            raise Exception('number:%s:%d' % (input_string, i))
        if buffer[0] == '.':
            dotted = True
        while True:
            i += 1
            try:
                c = input_string[i]
            except IndexError:
                break # fine stringa, ma non errore!
            if c in '0123456789':
                buffer.append(c)
            elif c == '.':
                if not dotted:
                    dotted = True
                    buffer.append(c)
                else:
                    raise Exception('number:%s:%d' % (input_string, i))
            else:
                break
    return input_string, i

def constant(input_string, i=0):
    try:
        c = input_string[i]
    except IndexError:
        raise Exception('constant:%s:%d' % (input_string, i))
    if c in 'xy':
        return input_string, i+1
    raise Exception('constant:%s:%d' % (input_string, i))

def ask(question_string, validate):
    return validate(raw_input(question_string))

def validate_function(input_string):
    """
        EXPR = TERM | TERM ( '+' | '-' ) TERM
        TERM = EXPTERM | EXPTERM ( '*' | '/' ) EXPTERM
        EXPTERM = FACTOR | FACTOR '^' FACTOR
        FACTOR = ( '+' | '-' )? ( NUMBER | CONSTANT ) | "(" EXPR ")"
        NUMBER = [0-9]+
        CONSTANT = 'x' | 'y'
    """
    validated_string, i = expr(input_string)
    return eval('lambda x, y: %s' % validated_string)

def validate_values(input_string):
    """values are a range input in the form [number : number : number ]"""
    MALFORMED_STRING = Exception('malformed string')
    if not input_string:
        raise Exception('empty string')
    if input_string[0] != '[':
        raise MALFORMED_STRING
    j = 1
    i = 1
    try:
        while input_string[j] != ':':
            j += 1
    except IndexError:
        raise MALFORMED_STRING
    try:
        range_begin = int(input_string[i:j])
    except ValueError:
        raise MALFORMED_STRING
    j += 1
    i = j
    try:
        while input_string[j] != ':':
            j += 1
    except IndexError:
        raise MALFORMED_STRING
    try:
        range_end = int(input_string[i:j])
    except ValueError:
        raise MALFORMED_STRING
    j += 1
    i = j
    try:
        while input_string[j] != ']':
            j += 1
    except IndexError:
        raise MALFORMED_STRING
    try:
        range_pass = int(input_string[i:j])
    except ValueError:
        raise MALFORMED_STRING
    return range(range_begin, range_end, range_pass)

def plot(function, x_values, y_values):
    for y in y_values:
        for x in x_values:
            print "%4d" % function(x, y),
        print

def main():
    from sys import argv
    if len(argv) == 4:
        function = validate_function(argv[1])
        x_values = validate_values(argv[2])
        y_values = validate_values(argv[3])
    else:
        function = ask("f(x, y) = ", validate_function)
        x_values = ask("[x0:x1:pass] ", validate_values)
        y_values = ask("[y0:y1:pass] ", validate_values)
    plot(function, x_values, y_values)

def test_number():
    for input in '', '.', '.0', '0.', '123', '1.2.3', '321', '154322.123', 'x':
        try:
            output = number(input, 0)
        except Exception as e:
            output = e
        print '%r -> %r' % (input, output)

def test_constant():
    for input in [(c, 0) for c in ('x','y','xy','','(x)','y^2')] + [('3x', 1)]:
        try:
            output = constant(*input)
        except Exception as e:
            output = e
        print '%r -> %r' % (input, output)

if __name__ == '__main__':
    main()
