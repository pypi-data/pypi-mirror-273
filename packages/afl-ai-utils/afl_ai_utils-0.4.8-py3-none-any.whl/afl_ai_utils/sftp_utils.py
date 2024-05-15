import os
import paramiko
import pandas as pd
from io import StringIO
import traceback

class SFTPUtils:
    def __init__(self, host, username, password, port):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
    def read_from_sftp(self):
        return

    def write_to_sftp_server(self, remote_path: str, dataframe: pd.DataFrame):
        try:
            csv_string = dataframe.to_csv(index=False)

            # Create an SSH client instance
            ssh_client = paramiko.SSHClient()

            # Automatically add the host keys
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the SSH server
            ssh_client.connect(self.host, self.port, self.username, self.password)

            # Create an SFTP session
            sftp = ssh_client.open_sftp()

            csv_buffer = StringIO(csv_string)

            # Write data to a file on the remote server
            with sftp.file(remote_path, "w") as file:
                file.write(csv_buffer.getvalue())

            # Close the SFTP session and SSH connection
            sftp.close()
            ssh_client.close()

            print("Data written successfully to", remote_path)
        except Exception as e:
            print("Error:", str(e) , "---> ", traceback.format_exc())
