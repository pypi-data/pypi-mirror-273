import requests
import os
import time
import logging
import threading

class Streamer:
    def __init__(self, url, file_path, CHUNK_SIZE=65536, WATCH_INTERVAL=0.5, WATCH_TIMEOUT=60, metadata=None, logging_level=logging.CRITICAL):
        self.url = url
        self.file_path = file_path
        self._CHUNK_SIZE = CHUNK_SIZE
        self._WATCH_INTERVAL = WATCH_INTERVAL
        self._WATCH_TIMEOUT = WATCH_TIMEOUT
        self._file_exists = False
        self._streaming_ongoing = False
        self._metadata = metadata or {}
        self._configure_logger(logging_level)
        self.logger.info('Streamer initialized')
        self._thread = None

    def _configure_logger(self, logging_level):
        self.logger = logging.getLogger('Streamer')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging_level)

    def start(self):
        self.logger.info('Starting')
        self._streaming_ongoing = True
        self._thread = threading.Thread(target=self._stream)
        self._thread.start()

    def _stream(self):
        if not self._file_exists and not self._check_file_exists():
            self.logger.info('Waiting for file to be created')
            while not self._file_exists and self._streaming_ongoing:
                self.logger.info('Still waiting for file to be created ...')
                time.sleep(self._WATCH_INTERVAL)
                if self._check_file_exists():
                    self.logger.info('File created')
                    self._file_exists = True

        if not self._streaming_ongoing:
            self.logger.info('Streaming stopped before it started')
            return

        self.logger.info('Starting streaming')
        headers = {f'X-Metadata-{k}': v for k, v in self._metadata.items()}
        self.logger.info('Sending request with metadata: %s', headers)
        with requests.Session() as session:
            with open(self.file_path, 'rb') as file:
                try:
                    response = session.post(self.url, data=self._stream_chunks(file), headers=headers, stream=True)
                    self.logger.info('Response status: %d', response.status_code)
                    for chunk in response.iter_content(chunk_size=1024):
                        if not self._streaming_ongoing:
                            self.logger.info('Streaming stopped during response iteration')
                            break
                        self.logger.debug('Received chunk: %s', chunk)
                except requests.RequestException as e:
                    self.logger.error('Request failed: %s', e)

    def stop(self):
        self.logger.info('Stopping streamer')
        self._streaming_ongoing = False
        if self._thread:
            self._thread.join()
            self.logger.info('Streaming thread joined')

    def _stream_chunks(self, file):
        self.logger.debug('Streaming chunks, ongoing: %s', self._streaming_ongoing)
        while self._streaming_ongoing:
            current_pos = file.tell()
            chunk = file.read(self._CHUNK_SIZE)
            if chunk:
                self.logger.debug('Yielding chunk of size: %d from position: %d', len(chunk), current_pos)
                yield chunk
            else:
                self.logger.info('No data, sleeping...')
                time.sleep(self._WATCH_INTERVAL)
                file.seek(current_pos)

        self.logger.info('Stopped streaming chunks due to _streaming_ongoing being False')

    def _check_file_exists(self):
        exists = os.path.exists(self.file_path)
        self.logger.info('Checking if file exists (%s): %s', self.file_path, exists)
        return exists
