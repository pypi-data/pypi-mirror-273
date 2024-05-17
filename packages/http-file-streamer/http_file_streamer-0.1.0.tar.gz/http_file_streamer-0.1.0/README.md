# My Streamer Package

A Python package for streaming and receiving files with additional metadata.

## Features

- Stream files to a specified URL.
- Receive files and save them locally or in memory.
- Supports metadata in the headers.
- Configurable logging.

## Installation

You can install the package using `pip`:

```bash
pip install my_streamer_package
```

## Usage

### Streamer

The `Streamer` class is used to stream files to a specified URL.

```python
from src import Streamer
import logging

url = "http://example.com/upload"
file_path = "/path/to/your/file.txt"
metadata = {"key1": "value1", "key2": "value2"}

streamer = Streamer(url, file_path, metadata=metadata, logging_level=logging.INFO)
streamer.start()

# To stop streaming
streamer.stop()
```

### Receiver

The `Receiver` class is used to receive files from a stream.

```python
from src import Receiver
import logging

headers = {"X-Metadata-key1": "value1", "X-Metadata-key2": "value2"}
stream = some_stream_source()  # This should be an iterable yielding byte chunks

receiver = Receiver(headers, stream, save_path="/path/to/save/file.txt", logging_level=logging.INFO)

# Get metadata
metadata = receiver.get_metadata()

# Check if streaming is ongoing
is_streaming = receiver.is_streaming()

# Get the length of the received content
content_length = receiver.get_content_length()

# Get the received file data
file_data = receiver.get_file_data()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## Author

[Babak Zarrinbal](https://github.com/babakzarrinbal)

