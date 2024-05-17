import os


def get_meta_str() -> str:

    pipefd = os.pipe()

    pid = os.fork()

    if 0 == pid:

        os.close(pipefd[0])

        os.dup2(pipefd[1], 1)

        os.close(pipefd[1])

        argv = ['./meta.sh']

        os.execve(argv[0], argv, os.environ)

        assert False, 'os.execve(...) returned, which is unexpected'

    assert 0 < pid

    os.close(pipefd[1])

    wait_pid, retcode_raw = os.wait()

    assert wait_pid == pid

    retcode = retcode_raw >> 8

    assert 0 == retcode

    meta_bytes = b''
    while True:
        byte = os.read(pipefd[0], 1)
        if 1 == len(byte):
            meta_bytes += byte
        else:
            assert 0 == len(byte)
            break

    meta_str = meta_bytes.decode('utf-8')

    return meta_str



