# Simple helper functions for input and output.

def read_params_from_file(filename):
    converters = {'categorical':str, 'integer':int, 'real':float}
    fp = open(filename, 'r')
    params = {}
    for line in fp:
        words = line.strip('\n').split(':')
        params[words[0]] = converters[words[1]](words[2])
    fp.close()
    return params


def write_measures_to_file(filename, measures):
    fp = open(filename, 'w')
    for measure in measures:
        print(measure, measures[measure], file=fp)
    fp.close()
    return

