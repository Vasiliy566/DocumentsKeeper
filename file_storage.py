from os import listdir


class FileStorage:
    def __init__(self, file_path):
        self.file_path = file_path

    def upload_file(self, name, content: bytes):
        with open(f"{self.file_path}/{name}", mode="wb") as file:
            file.write(content)

    def read_all_filenames(self):
        return listdir(self.file_path)

    def get_file_by_name(self, name):
        existed_files = self.read_all_filenames()
        if name not in existed_files:
            raise Exception("File not found.")

        with open(f"{self.file_path}/{name}", mode="rb") as file:
            return file.read()
