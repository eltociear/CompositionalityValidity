# Copyright (c) Meta Platforms, Inc. and affiliates All Rights Reserved

"""Reformat datasets in NQG as input formats required by OpenNMT."""
# This is different from the original reformat data only in the amount of columns in input tsv files: COGS has a third column, while data format in NQG only has two columns.
import argparse
import os

# Prespecified set of file names in the dataset.
_DATASET_FILENAMES = ['train', 'test']

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_path', default=None, type=str, required=True,
                        help='Path to directory containing the dataset.')
    parser.add_argument('--output_path', default=None, type=str, required=True,
                        help='Path to save the output data to.')
    args = parser.parse_args()

    source_vocab = set()
    target_vocab = set()

    # Create a new directory if the specified output path does not exist.
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    for filename in _DATASET_FILENAMES:
        with open(os.path.join(args.input_path, f'{filename}.tsv')) as f:
            data = f.readlines()

        source_lines = []
        target_lines = []

        # Starting from 1 to skip the headers
        for line in data[1:]:
            source, target = line.rstrip('\n').split('\t')
            source_lines.append('{}\n'.format(source))
            target_lines.append('{}\n'.format(target))
            source_vocab.update(source.split())
            target_vocab.update(target.split())

        # Write the datapoints to source and target files.
        with open(os.path.join(args.output_path, f'{filename}_source.txt'), 'w') as wf:
            wf.writelines(source_lines)

        with open(os.path.join(args.output_path, f'{filename}_target.txt'), 'w') as wf:
            wf.writelines(target_lines)

    # Write the vocabulary files.
    with open(os.path.join(args.output_path, 'source_vocab.txt'), 'w') as wf:
        for w in list(source_vocab):
            wf.write(w)
            wf.write('\n')

    with open(os.path.join(args.output_path, 'target_vocab.txt'), 'w') as wf:
        for w in list(target_vocab):
            wf.write(w)
            wf.write('\n')

    print(f'Reformatted and saved COGS data to {args.output_path}.')


if __name__ == '__main__':
    main()
