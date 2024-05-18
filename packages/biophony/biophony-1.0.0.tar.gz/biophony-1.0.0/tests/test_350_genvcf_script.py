# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
import os
import subprocess
import pytest
import biophony

# Get test directory
@pytest.fixture
def test_dir():
    script_path = os.path.realpath(__file__)
    testdir = os.path.dirname(script_path)
    return testdir

# Get wrk dir
@pytest.fixture
def wrk_dir(test_dir):
    wrk_dir = os.path.join(test_dir, 'wrk')
    os.makedirs(wrk_dir, exist_ok=True)
    return wrk_dir

# Get cmd to test
@pytest.fixture
def cmd():
    return ['python', '-c', 'import biophony; biophony.vcfgen_cli()']

# Create input FASTA file
@pytest.fixture
def fasta_file(wrk_dir):
    fasta_file = os.path.join(wrk_dir, 'genvcf_test.fasta')
    if not os.path.exists(fasta_file):
        with open(fasta_file, 'w', encoding="utf-8") as f:
            writer = biophony.FastaWriter(f, header = False)
            gen = biophony.BioSeqGen()
            for seq in gen:
                writer.write_bio_seq(seq)
    return fasta_file

def test_help(cmd):
    for opt in ['-h', '--help']:
        with subprocess.Popen(cmd + [opt], stdout=subprocess.PIPE) as proc:
            assert proc.wait() == 0

def test_no_mutation(cmd, fasta_file):
    opt = ['-f', fasta_file]
    with subprocess.Popen(cmd + opt, stdout=subprocess.PIPE) as proc:
        assert proc.wait() == 1 # Fails because no mutation were asked

def test_insertions(cmd, fasta_file):
    opt = ['-f', fasta_file, '-i', str(0.5)]
    with subprocess.Popen(cmd + opt, stdout=subprocess.PIPE) as proc:
        assert proc.wait() == 0
        lines = proc.stdout.readlines()
        for line in lines:
            assert line.startswith(b"#") or line.find(b"\tSVTYPE=INS;") >= 0

def test_deletions(cmd, fasta_file):
    opt = ['-f', fasta_file, '-d', str(0.5)]
    with subprocess.Popen(cmd + opt, stdout=subprocess.PIPE) as proc:
        assert proc.wait() == 0
        lines = proc.stdout.readlines()
        for line in lines:
            assert line.startswith(b"#") or line.find(b"\tSVTYPE=DEL;") >= 0

def test_mutations(cmd, fasta_file):
    opt = ['-f', fasta_file, '-m', str(0.5)]
    with subprocess.Popen(cmd + opt, stdout=subprocess.PIPE) as proc:
        assert proc.wait() == 0
        lines = proc.stdout.readlines()
        for line in lines:
            assert line.startswith(b"#") or line.find(b"SVTYPE;") < 0
