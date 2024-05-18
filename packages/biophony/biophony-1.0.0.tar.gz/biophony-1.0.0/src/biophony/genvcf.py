# pylint: disable=missing-module-docstring
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

def read_args() -> argparse.Namespace:
    # pylint: disable=missing-function-docstring
    parser = argparse.ArgumentParser(description='Generates VCF files.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--fasta-file', dest='fasta_file', type=str,
                        default='-',
                        help='A FASTA file to use for generating the VCF file.')
    parser.add_argument('-m', '--snp-rate', dest='snp_rate', type=float,
                        default=0.0,
                        help='The probability of mutation of one base.')
    parser.add_argument('-i', '--ins-rate', dest='ins_rate', type=float,
                        default=0.0,
                        help='The probability of insertion at one base.')
    parser.add_argument('-d', '--del-rate', dest='del_rate', type=float,
                        default=0.0,
                        help='The probability of deletion of one base.')
    args = parser.parse_args()
    return args

def vcfgen_cli() -> None:
    """VCF generation CLI.
    """

    args = read_args()

    # Create temp folder
    old_dir = os.getcwd()
    tmp_dir = tempfile.mkdtemp()

    try:
        # Write FASTA data if received from stdin
        if args.fasta_file == '-':
            args.fasta_file = os.path.join(tmp_dir, 'seq.fasta')
            with open(args.fasta_file, 'w', encoding="utf-8") as f:
                for line in sys.stdin:
                    f.write(line)

        # Enter temp folder
        os.chdir(tmp_dir)

        # Call mutation-simulator script
        cmd = ["mutation-simulator", "-q", "-o", "variant", args.fasta_file,
               "args", "-sn", str(args.snp_rate), "-de", str(args.del_rate),
               "-in", str(args.ins_rate)]
        with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
            exit_code = proc.wait()
            assert exit_code == 0

        # Get generated VCF file
        with open(os.path.join(tmp_dir, 'variant_ms.vcf'), 'r',
                  encoding="utf-8") as f:
            for line in f:
                sys.stdout.write(line)

        # Leave temp folder
        os.chdir(old_dir)

    finally:
        # Delete temp folder
        shutil.rmtree(tmp_dir)

    sys.exit(0)

if __name__ == '__main__':
    vcfgen_cli()
