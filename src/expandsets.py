#!/usr/bin/env python3
#
# Copyright 2010 Paolo Martini <paolo.cavei@gmail.com>

import argparse
import sys
from sys import stdin
from itertools import chain

def parse_column_indexes(args):
    indexes = []
    for arg in args:
        try:
            value = int(arg)
            if value <= 0:
                raise ValueError
        except ValueError:
            exit(f'Invalid column index: {arg}')

        indexes.append(value - 1)

    indexes.sort()
    return indexes

def build_matrix(tokens, column_indexes, separator):
    matrix = [None] * len(column_indexes)
    for midx, cidx in enumerate(column_indexes):
        matrix[midx] = tokens[cidx].split(separator)
    return matrix

def iterate_matrix(matrix):
    counter = [0] * len(matrix)

    def increment():
        for i in range(len(matrix)):
            counter[i] += 1
            if counter[i] < len(matrix[i]):
                break
            else:
                counter[i] = 0
        else:
            return False
        return True

    while True:
        yield [matrix[i][counter[i]] for i in range(len(matrix))]
        if not increment():
            break

def main():
    parser = argparse.ArgumentParser(description='''
        Given a COLUMN with different entities separated by a specific string
        the program expands them into multiple rows.
        If more than 1 COLUMN is specified, the cartesian product of the two sets
        is returned.
    ''')
    
    parser.add_argument('columns', metavar='COLUMN', type=int, nargs='+', help='Columns to expand')
    parser.add_argument('-s', '--separator', type=str, dest='separator', default=";", help='Indicate the separator for multiple values of the same key in input (default: %(default)s)', metavar='SEPARATOR')
    parser.add_argument('-p', '--pairs', dest='pairs', action="store_true", help='If exactly two columns to expand are indicated, do not return the cartesian product of the two sets but assume that the sets in the two columns have the same size and couple the i-th element of the first set with the i-th element of the second set')
    parser.add_argument('-t', '--tuples', dest='tuples', action="store_true", help='Same as --pairs, kept for backward compatibility')
    options = parser.parse_args()

    if options.tuples:
        options.pairs = True

    if len(options.columns) < 1:
        exit('Unexpected argument number.')

    column_indexes = parse_column_indexes(options.columns)
    firstline = stdin.readline()
    n = len(firstline.rstrip().split('\t'))

    if options.pairs and len(column_indexes) != 2:
        exit("If --pairs is indicated then exactly 2 columns to expand are required")

    try:
        for idx, line in enumerate(chain([firstline], stdin)):
            tokens = line.rstrip('\r\n').split('\t')
            if len(tokens) <= column_indexes[-1]:
                exit(f'Insufficient column number at line {idx + 1}.')

            matrix = build_matrix(tokens, column_indexes, options.separator)
            if not options.pairs:
                for values in iterate_matrix(matrix):
                    for value, cidx in zip(values, column_indexes):
                        tokens[cidx] = value
                    print('\t'.join(tokens))
            else:
                if len(matrix[0]) != len(matrix[1]):
                    exit(f"The two sets to expand must have the same size when --pairs is indicated ({len(matrix[0])} - {len(matrix[1])})")

                for values in zip(matrix[0], matrix[1]):
                    tokens[column_indexes[0]] = values[0]
                    tokens[column_indexes[1]] = values[1]
                    print('\t'.join(tokens))
    except BrokenPipeError:
        pass

if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        sys.stderr.close()
        sys.exit(1)
