import os
from biotools import accessoryfunctions
# Jellyfish is a bit of a pain due to it needing uncompressed input - I'll do some figuring on how I want to
# get it implemented and come back to it.


def count(forward_in, reverse_in='NA', kmer_size=31, count_file='mer_counts.jf', hash_size='100M', options=''):
    """
    Runs jellyfish count to kmerize reads to a desired kmer size.
    :param forward_in: Forward input reads or fasta file. Can be uncompressed or gzip compressed.
    :param reverse_in: Reverse input reads. Found automatically if in same folder as forward and R1/R2 naming convention
    used.
    :param kmer_size: Kmer size to get jellyfish to use. Default 31.
    :param count_file: File to have jellyfish output mer counts to. Default mer_counts.jf
    :param hash_size: Hash size. Should be suitable for most, if not all, bacterial genomes, and as of jellyfish2 should
    adjust to be larger automatically if needed.
    :param options: Other options to pass to jellyfish. Input should be a string, with options typed as they would be
    on the command line.
    :return: Stdout and stderr from calling jellyfish.
    """
    create_uncompressed = False
    to_remove = list()
    if os.path.isfile(forward_in.replace('R1', 'R2')) and reverse_in == 'NA':
        reverse_in = forward_in.replace('R1', 'R2')
        if forward_in.endswith('.gz'):
            forward_in = accessoryfunctions.uncompress_gzip(forward_in)
            create_uncompressed = True
            to_remove.append(forward_in)
        if reverse_in.endswith('.gz'):
            reverse_in = accessoryfunctions.uncompress_gzip(reverse_in)
            create_uncompressed = True
            to_remove.append(reverse_in)
        cmd = 'jellyfish count -m {} -C -s {} -o {} {} -F 2 {} {}'.format(str(kmer_size), hash_size, count_file,
                                                                          options, forward_in, reverse_in)
    elif reverse_in == 'NA':
        cmd = 'jellyfish count -m {} -C -s {} -o {} {} {}'.format(str(kmer_size), hash_size, count_file,
                                                                  options, forward_in)
    else:
        cmd = 'jellyfish count -m {} -C -s {} -o {} {} -F 2 {} {}'.format(str(kmer_size), hash_size, count_file,
                                                                          options, forward_in, reverse_in)
    out, err = accessoryfunctions.run_subprocess(cmd)
    if create_uncompressed:
        for item in to_remove:
            os.remove(item)
    return out, err


def dump(mer_file, output_file='counts.fasta', options=''):
    """
    Dumps output from jellyfish count into a human-readable format.
    :param mer_file: Output from jellyfish count.
    :param output_file: Where to store output. Default counts.fasta
    :param options: Other options to pass to jellyfish. Input should be a string, with options typed as they would be
    on the command line.
    :return: Stdout and stderr from calling jellyfish.
    """
    cmd = 'jellyfish dump {} -o {} {}'.format(mer_file, output_file, options)
    out, err = accessoryfunctions.run_subprocess(cmd)
    return out, err
