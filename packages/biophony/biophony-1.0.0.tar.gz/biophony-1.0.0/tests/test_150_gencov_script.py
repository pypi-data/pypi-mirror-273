# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import os
import re
import subprocess

script_path = os.path.realpath(__file__)
testdir = os.path.dirname(script_path)
cmd = ['python', '-c', 'import biophony; biophony.covgen_cli()']

def test_help():
    for opt in ['-h', '--help']:
        with subprocess.Popen(cmd + [opt], stdout=subprocess.PIPE) as proc:
            assert proc.wait() == 0

def test_default():
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        (output, _) = proc.communicate()
        exit_code = proc.wait()
        assert exit_code == 0
        assert len(output.rstrip().split(b"\n")) == 10001

def test_custom_pos_number():
    for n in [0, 1, 5, 10, 11]:
        with subprocess.Popen(cmd + ["-p", f"0-{n}"],
                              stdout=subprocess.PIPE) as proc:
            exit_code = proc.wait()
            assert exit_code == 0
            lines = proc.stdout.readlines()
            assert len(lines) == n + 1
            for i, line in enumerate(lines):
                assert f"chr1\t{i}\t0\n" == line.decode("utf-8")

def test_custom_chromosome():
    n = 10
    chrom = 4
    with subprocess.Popen(cmd + ["-c", f"{chrom}", "-p", f"0-{n}"],
                          stdout=subprocess.PIPE) as proc:
        exit_code = proc.wait()
        assert exit_code == 0
        lines = proc.stdout.readlines()
        assert len(lines) == n + 1
        for i, line in enumerate(lines):
            assert f"chr{chrom}\t{i}\t0\n" == line.decode("utf-8")

def test_custom_depth():
    n = 10
    depth = 6
    with subprocess.Popen(cmd + ["-d", f"{depth}", "-p", f"0-{n}"],
                          stdout=subprocess.PIPE) as proc:
        exit_code = proc.wait()
        assert exit_code == 0
        lines = proc.stdout.readlines()
        assert len(lines) == n + 1
        for i, line in enumerate(lines):
            assert f"chr1\t{i}\t{depth}\n" == line.decode("utf-8")

def test_custom_depth_change_rate():
    n = 50
    depth_min = 6
    depth_max = 10
    depth_change_rate = 0.5
    with subprocess.Popen(cmd + ["-d", f"{depth_min}-{depth_max}",
                          "-r", f"{depth_change_rate}",
                          "-p", f"0-{n}"],
                          stdout=subprocess.PIPE) as proc:
        exit_code = proc.wait()
        assert exit_code == 0
        lines = proc.stdout.readlines()
        assert len(lines) == n + 1
        depth_range = "|".join([str(x) for x in range(depth_min,
                                                      depth_max + 1)])
        for i, line in enumerate(lines):
            assert re.match(f"^chr1\t{i}\t({depth_range})$",
                            line.decode("utf-8"))

def test_custom_depth_start():
    n = 10
    depth = 1
    depth_start = 5
    with subprocess.Popen(cmd + ["-s", f"{depth_start}", "-d", f"{depth}",
                          "-p", f"0-{n}"],
                          stdout=subprocess.PIPE) as proc:
        exit_code = proc.wait()
        assert exit_code == 0
        lines = proc.stdout.readlines()
        assert len(lines) == n + 1
        for i, line in enumerate(lines):
            line = line.rstrip().decode("utf-8")
            if i < depth_start:
                assert f"chr1\t{i}\t0" == line
            else:
                assert f"chr1\t{i}\t{depth}" == line
