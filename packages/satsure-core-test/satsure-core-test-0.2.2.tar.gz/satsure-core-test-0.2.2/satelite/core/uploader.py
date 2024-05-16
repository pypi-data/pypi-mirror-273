import shutil
from pathlib import Path, PosixPath
from subprocess import Popen, PIPE


class UpLoader:

    def upload_folder(self, local_folder: PosixPath, bucket_name: str, prefix: str,
                      exclude: str = "*", include: str = "*", delete_local: bool = False):
        """
            to upload file in AWS
        :param local_folder:
        :param bucket_name:
        :param prefix:
        :param exclude:
        :param include:
        :param delete_local:
        :return:
        """
        command = f"""aws s3 cp "{local_folder}" "s3://{bucket_name}/{prefix}" --recursive --exclude "{exclude}" --include "{include}" --request-payer"""
        process = Popen(command, shell=True, stdout=PIPE)
        process.communicate()

        if delete_local:
            shutil.rmtree(Path(local_folder))
