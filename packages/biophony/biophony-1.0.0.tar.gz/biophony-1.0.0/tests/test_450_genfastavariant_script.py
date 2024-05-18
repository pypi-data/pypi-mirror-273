# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
import subprocess
import pytest

# Get cmd to test
@pytest.fixture
def cmd():
    return ['python', '-c', 'import biophony; biophony.fastavargen_cli()']

def test_help(cmd):
    for opt in ['-h', '--help']:
        with subprocess.Popen(cmd + [opt], stdout=subprocess.PIPE) as proc:
            assert proc.wait() == 0

def test_no_mutation(cmd):
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        assert proc.wait() == 0

def test_wrong_rate_sum(cmd):
    opt = ["-i", str(0.4), "-m", str(0.4), "-d", str(0.4)]
    with subprocess.Popen(cmd + opt, stdout=subprocess.PIPE) as proc:
        assert proc.wait() != 0 # Fails because sum of mutation rates > 1.0

def test_nb_sequences(cmd):
    for rate_opt in ["-m", "-d", "-i"]:
        opt = [rate_opt, str(0.5)]
        print(cmd+opt)
        with subprocess.Popen(cmd + opt, stdout=subprocess.PIPE) as proc:
            assert proc.wait() == 0
            lines = proc.stdout.readlines()
            n_seq = 0
            n_variants = 0
            for line in lines:
                print(line)
                if line.find(b">seq") >= 0:
                    n_seq += 1
                if line.find(b"_var") >= 0:
                    n_variants += 1
            assert n_seq == 10
            assert n_variants == 5
