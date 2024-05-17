from pathlib import Path
from typing import List, Literal, Optional, Tuple, Union

from huggingface_hub import snapshot_download


def test_error():
    import traceback

    try:
        1 / 0
    except Exception as e:
        print(f"repr(e): {repr(e)}")
        print(f"str(e): {str(e)}")
        print(f"e: {e}")

        print(f"\n ----------\ntraceback.print_exc(): {traceback.print_exc()}")

        print("\n ----------\nraise e")
        raise e


from typing import Union, overload


@overload
def iou(input: int) -> int: ...


@overload
def iou(input: str) -> str: ...


def iou(input: Union[str, int]) -> Union[str, int]:
    return input


from openi import download_file, download_model, download_model_file

filename = "archive.zip"
model_name = "ChatGLM2-6B"
repo_id = "FoundationModel/ChatGLM2-6B"


import time

# download_model(repo_id=repo_id, model_name=model_name, save_path="./test/chatglm2-6b")
# download_file(repo_id=repo_id, file=filename)
import openi

# openi.login(token="asdasjksdhak")


def print_wait():
    a = 5
    return a


a = print_wait()
print(a)
