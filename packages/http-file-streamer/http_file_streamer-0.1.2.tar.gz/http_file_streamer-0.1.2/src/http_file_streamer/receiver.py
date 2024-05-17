import os
import logging
import threading

class Receiver:
    def __init__(self, headers, stream, save_path=None, CHUNK_SIZE=65536, logging_level=logging.CRITICAL):
        self.headers = headers
        self.stream = stream
        self.save_path = save_path
        self.CHUNK_SIZE = CHUNK_SIZE
        self._metadata = {}
        self._content = bytearray()
        self._isStreaming = True
        self._configure_logger(logging_level)
        self.logger.info('Receiver initialized')
        self._prepare_save_path()
        self._thread = threading.Thread(target=self._process_request)
        self._thread.start()
        self.logger.info('Receiver started')

    def _configure_logger(self, logging_level):
        self.logger = logging.getLogger('Receiver')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging_level)

    def _prepare_save_path(self):
        if self.save_path:
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            self.logger.info(f'Created directory for save path: {self.save_path}')

    def _process_request(self):
        self.logger.info('Processing request')
        self._metadata = {key[11:]: value for key, value in self.headers.items() if key.startswith('X-Metadata-')}
        
        if self.save_path:
            with open(self.save_path, 'wb') as f:
                for chunk in self.stream:
                    if not chunk:
                        continue
                    self._content.extend(chunk)
                    f.write(chunk)
                    self.logger.debug(f'Wrote chunk to file: {self.save_path}')
        else:
            for chunk in self.stream:
                if not chunk:
                    continue
                self._content.extend(chunk)
                self.logger.debug('Appended chunk to content')

        self._isStreaming = False
        self.logger.info('Finished processing request')

    def get_metadata(self):
        self.logger.info('Returning metadata')
        return self._metadata

    def is_streaming(self):
        self.logger.info(f'Streaming status: {self._isStreaming}')
        return self._isStreaming

    def get_content_length(self):
        length = len(self._content)
        self.logger.info(f'Content length: {length}')
        return length

    def get_file_data(self):
        self.logger.info('Returning file data')
        return {
            "metadata": self._metadata,
            "file_binary_data": bytes(self._content)
        }
