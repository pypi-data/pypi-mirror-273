# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import os
import re
import subprocess

script_path = os.path.realpath(__file__)
testdir = os.path.dirname(script_path)
cmd = ['python', '-c', 'import biophony; biophony.fastagen_cli()']

def test_help():
    for opt in ['-h', '--help']:
        with subprocess.Popen(cmd + [opt], stdout=subprocess.PIPE) as proc:
            assert proc.wait() == 0

def test_default():
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        exit_code = proc.wait()
        assert exit_code == 0
        lines = proc.stdout.readlines()
        seq = ''
        for i, line in enumerate(lines):
            line = line.rstrip().decode("utf-8")
            if i < 1:
                assert line.startswith(";")
            elif i == 1:
                assert line == ">chr1"
            else:
                assert len(line) <= 80
                assert re.match(r"^[ACTG]+$", line)
                seq += line
        assert len(seq) == 1000

def test_custom_length():
    for seq_length in [0, 1, 79, 80, 81, 457]:
        with subprocess.Popen(cmd + ['-n', str(seq_length)],
                              stdout=subprocess.PIPE) as proc:
            exit_code = proc.wait()
            assert exit_code == 0
            lines = proc.stdout.readlines()
            seq = ''
            for i, line in enumerate(lines):
                line = line.rstrip().decode("utf-8")
                if i < 1:
                    assert line.startswith(";")
                elif i == 1:
                    assert line == ">chr1"
                else:
                    assert len(line) <= 80
                    assert re.match(r"^[ACTG]*$", line)
                    seq += line
            assert len(seq) == seq_length

def test_custome_seqid():
    with subprocess.Popen(cmd + ["-s", "foo"], stdout=subprocess.PIPE) as proc:
        exit_code = proc.wait()
        assert exit_code == 0
        lines = proc.stdout.readlines()
        seq = ''
        for i, line in enumerate(lines):
            line = line.rstrip().decode("utf-8")
            if i < 1:
                assert line.startswith(";")
            elif i == 1:
                assert line == ">foo1"
            else:
                assert len(line) <= 80
                assert re.match(r"^[ACTG]+$", line)
                seq += line
        assert len(seq) == 1000

def test_custom_elements():
    with subprocess.Popen(cmd + ["-e", "ZY"], stdout=subprocess.PIPE) as proc:
        exit_code = proc.wait()
        assert exit_code == 0
        lines = proc.stdout.readlines()
        seq = ''
        for i, line in enumerate(lines):
            line = line.rstrip().decode("utf-8")
            if i < 1:
                assert line.startswith(";")
            elif i == 1:
                assert line == ">chr1"
            else:
                assert len(line) <= 80
                assert re.match(r"^[YZ]+$", line)
                seq += line
        assert len(seq) == 1000

def test_custome_line_size():
    for line_size in [50, 100]:
        with subprocess.Popen(cmd + ["--line-size", str(line_size)],
                              stdout=subprocess.PIPE) as proc:
            exit_code = proc.wait()
            assert exit_code == 0
            lines = proc.stdout.readlines()
            seq = ''
            for i, line in enumerate(lines):
                line = line.rstrip().decode("utf-8")
                if i < 1:
                    assert line.startswith(";")
                elif i == 1:
                    assert line == ">chr1"
                else:
                    assert len(line) <= line_size
                    assert re.match(r"^[ACTG]+$", line)
                    seq += line
            assert len(seq) == 1000
