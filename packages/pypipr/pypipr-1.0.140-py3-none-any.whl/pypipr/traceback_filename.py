import traceback


def traceback_filename():
    """
    Mendapatkan filename dimana fungsi yg memanggil
    fungsi ini dipanggil.

    ```py
    print(traceback_filename())
    ```
    """
    return traceback.extract_stack()[-2].filename
