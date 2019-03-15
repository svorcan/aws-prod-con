import json
import os
import socket
import stat
from dataclasses import dataclass
from paramiko import SFTPClient, Transport
from paramiko.ssh_exception import SSHException
from producer.exceptions import SFTPError


@dataclass
class Data:
    """Class representing one downloaded file."""
    file_name: str
    json: str


class SFTPHandler:
    """Class containing logic for necessary SFTP operations."""
    def __init__(self, config):
        try:
            transport = Transport((config.SFTP_HOST, config.SFTP_PORT))
            transport.connect(username=config.SFTP_USERNAME, password=config.SFTP_PASSWORD)
            self.sftp_client = SFTPClient.from_transport(transport)
        except (SSHException, socket.error) as e:
            raise SFTPError(f'SFTP connection failed due to: {e}.')

        self.path = config.SFTP_PATH
        self.temp_file_path = config.TEMP_FILE_PATH

    def retrieve_data(self):
        """Retrieve yielded items from provided directory on SFTP server.
           Files which are unable to download at the moment are skipped and left for the next processing cycle."""
        file_names = self.sftp_client.listdir(path=self.path)

        for file_name in file_names:
            try:
                if not self._is_json_file(file_name):
                    continue

                self.sftp_client.get(file_name, localpath=self.temp_file_path)

                try:
                    with open(self.temp_file_path) as downloaded_file:
                        json_data = json.load(downloaded_file)
                        yield Data(file_name=file_name, json=json_data)
                finally:
                    os.remove(self.temp_file_path)
            except (SSHException, socket.error) as e:
                # TODO: implement actual logging mechanism
                print(f'Failed to download file \'{file_name}\' due to: {e}.')

    def remove_file(self, file_name):
        """Deletes file with provided name from SFTP server."""
        file_path = self._get_file_path(file_name)
        try:
            self.sftp_client.remove(file_path)
        except (SSHException, socket.error) as e:
            raise SFTPError(f'Failed to delete \'{file_name}\' file due to: {e}.')

    def _get_file_path(self, file_name):
        """Gets remote path for provided file name."""
        return os.path.join(self.path, file_name)

    def _is_json_file(self, file_name):
        """Checks if provided file is JSON file."""
        file_extension = os.path.splitext(file_name)[1].lower()
        if file_extension != '.json':
            return False

        file_path = self._get_file_path(file_name)
        file_stat = self.sftp_client.stat(file_path)
        return stat.S_ISREG(file_stat.st_mode)
