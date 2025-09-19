import pandas as pd
from pymavlink import DFReader
import time

def bin_to_dataframe_optimized(file_path: str) -> dict:
    """
    Optimized reader for ArduPilot/PX4 .bin logs.
    Returns a dictionary of DataFrames, one per message type.
    """
    log = DFReader.DFReader_binary(file_path)
    data = {}  # store messages per type

    batch_size = 10000
    batch = []

    while True:
        msg = log.recv_msg()
        if msg is None:
            break
        batch.append(msg)

        if len(batch) >= batch_size:
            _process_batch(batch, data)
            batch = []

    # process remaining messages
    if batch:
        _process_batch(batch, data)

    # Convert lists to DataFrames
    dfs = {msg_type: pd.DataFrame(msg_list) for msg_type, msg_list in data.items()}

    return dfs

def _process_batch(batch, data):
    """Helper to append batch messages to the per-type dictionary"""
    for msg in batch:
        msg_type = msg.get_type()
        if msg_type not in data:
            data[msg_type] = []
        data[msg_type].append(msg.to_dict())

if __name__ == "__main__":
    file_path = "1980-01-08 09-44-08.bin"  # <-- replace with your log
    time_start = time.time()
    dfs = bin_to_dataframe_optimized(file_path)
    time_end = time.time()
    print(f"Time taken: {time_end - time_start} seconds")

    print(dfs.keys())

    print(len(dfs.keys()))













































