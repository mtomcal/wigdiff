"""
WigDiff

Comparing the difference in values between two .wig files and outputting a GFF file

"""
import sys
import re

def read_file(filename):
    with open(filename, 'r') as reader:
        return reader.readlines()
    raise IOError

def file_loop(diff_fold):
    try:
        wig_a = read_file(sys.argv[1])
        wig_b = read_file(sys.argv[2])
    except IndexError:
        print """wigdiff.py
Comparing the difference in values between two .wig files and outputting a GFF file

Usage:
    python wigdiff.py <a.wig> <b.wig> [difference_cutoff]

[difference_cutoff] defaults to 0.10

Example:
    python wigdiff.py file1.wig file2.wig 0.20
"""
        exit(1)
    try:
        calculate_diff(wig_a, wig_b, diff_fold)
    except IndexError:
        pass

def calculate_diff(wig_a, wig_b, diff_fold):
    range_start = 1
    range_stop = 500
    expr = re.compile(r'chrom\=([\w|\.]+)')
    name = ""
    for line in range(0, len(wig_a)):
        match = expr.search(wig_a[line])
        if match:
            name = match.group(1)
            range_start = 1
            range_stop = 500
        else:
            wig_a_value = float(wig_a[line])
            wig_b_value = float(wig_b[line])
            diff = wig_a_value - wig_b_value
            if abs(diff) > diff_fold:
                print "%s\t%d\t%d\t%f" % (name, range_start, range_stop, diff)
            range_start += 500
            range_stop += 500

def main():
    diff_fold = 0.10
    try:
        diff_fold = float(sys.argv[3])
    except IndexError:
        pass
    file_loop(diff_fold)

main()
