import hashlib
import json
import os
import pathlib
import tempfile
import typing
import zipfile


__all__ = [
    'LONG_LONG_SIZE',
    'INTEGER_SIZE',
    'TestCase',
    'Problem'
]


LONG_LONG_SIZE = 2305843009213693952
INTEGER_SIZE = 2147483648


class TestCase:
    def __init__(self, id: str, input: str, output: str, strip=True) -> None:
        self.id = id
        self.input = input.strip() if strip else input
        self.output = output.strip() if strip else output

    @property
    def input_size(self) -> int:
        """Length of input data."""
        return len(self.input)

    @property
    def output_size(self) -> int:
        """Length of output data."""
        return len(self.output)

    @property
    def input_name(self) -> str:
        """A filename for the input."""
        return f'{self.id}.in'

    @property
    def output_name(self) -> str:
        """A filename for the output."""
        return f'{self.id}.out'

    @property
    def stripped_output_md5(self) -> str:
        md5 = hashlib.md5()
        md5.update(self.output.strip().encode())
        return md5.hexdigest()

    def as_dict(self) -> dict:
        return {
            "stripped_output_md5": self.stripped_output_md5,
            "input_size": self.input_size,
            "output_size": self.output_size,
            "input_name": self.input_name,
            "output_name": self.output_name,
        }

    def extract_as_file(self, dir='./') -> None:
        """Save testcase as `input_name` and `output_name` in a specific directory."""
        dir_path = pathlib.Path(dir)
        with open(dir_path / self.input_name, 'w') as f:
            f.write(self.input)
        with open(dir_path / self.output_name, 'w') as f:
            f.write(self.output)


class Problem:
    def __init__(self, title: str) -> None:
        self.title = title
        self.spj = False
        self.testcases: typing.Dict[str, TestCase] = {}

    def add_testcase(self, testcase: TestCase):
        """Add a testcase for this problem."""
        self.testcases[testcase.id] = testcase

    def as_dict(self) -> dict:
        return {
            "spj": self.spj,
            "testcases": {
                key: val.as_dict() for key, val in self.testcases.items()
            },
        }

    def extract_as_zip(self, file="./problem.zip") -> None:
        """Save problem as .zip file"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_path = pathlib.Path(file)
            dir_path = pathlib.Path(tmp_dir)
            info_filename = 'info'

            for testcase in self.testcases.values():
                testcase.extract_as_file(dir=dir_path)

            with open(dir_path / info_filename, 'w') as f:
                json.dump(self.as_dict(), f, ensure_ascii=True)

            with zipfile.ZipFile(zip_path, 'w') as fzip:
                for testcase in self.testcases.values():
                    fzip.write(filename=dir_path / testcase.input_name, arcname=testcase.input_name)
                    fzip.write(filename=dir_path / testcase.output_name, arcname=testcase.output_name)
                fzip.write(filename=dir_path / info_filename, arcname=info_filename)
