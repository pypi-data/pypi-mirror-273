import hashlib
import io


class TestCase:
    def __init__(self) -> None:
        self._input = io.TextIOWrapper(io.BytesIO())
        self._output = io.TextIOWrapper(io.BytesIO())

    @property
    def input(self) -> io.TextIOWrapper:
        """input stream."""
        return self._input

    @property
    def output(self) -> io.TextIOWrapper:
        """output stream."""
        return self._output

    @property
    def input_text(self) -> str:
        """input data."""
        return self._read_stream(self._input)

    @property
    def output_text(self) -> str:
        """output data."""
        return self._read_stream(self._output)

    @property
    def input_size(self) -> int:
        """Length of input data."""
        return self._size_of_stream(self._input)

    @property
    def output_size(self) -> int:
        """Length of output data."""
        return self._size_of_stream(self._output)

    @property
    def stripped_output_md5(self) -> str:
        md5 = hashlib.md5()
        md5.update(str(self.output_text).strip().encode())
        return md5.hexdigest()

    def _read_stream(self, stream: io.TextIOBase) -> str:
        cursor = stream.tell()
        stream.seek(0, io.SEEK_SET)
        text = stream.read()
        stream.seek(cursor, io.SEEK_SET)
        return text

    def _size_of_stream(self, stream: io.TextIOBase) -> str:
        return len(self._read_stream(stream))
