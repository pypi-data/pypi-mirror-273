import time
from datetime import datetime, timedelta


def threshold():
    return datetime.utcnow().strftime('%Y-%m-%d')

def assert_files_equal(file1_path, file2_path):
    with open(file1_path, 'r') as file1:
        content1 = file1.read()

    with open(file2_path, 'r') as file2:
        content2 = file2.read()

    assert content1 == content2, f"Contents of the files {file1_path} and {file2_path} file are not equal"

class Utils:
    def __init__(self, chariot):
        self.chariot = chariot

    def wait_for_key(self, key, timeout=60, interval=5):
        start_time = time.time()
        while time.time() - start_time < timeout:
            print(f"Trying to get response for my {key}")
            response = self.chariot.my(key)
            if response:
                return response
            time.sleep(interval)

    def add_seed(self, seed):
        return self.chariot.add_asset(seed, "AA")

