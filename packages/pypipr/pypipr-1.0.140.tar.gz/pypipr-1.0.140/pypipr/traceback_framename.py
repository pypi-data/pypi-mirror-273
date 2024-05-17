import traceback


def traceback_framename():
    """
    Mendapatkan frame name dimana fungsi yg memanggil
    fungsi ini dipanggil.

    ```py
    print(traceback_framename())
    ```
    """
    return traceback.extract_stack()[-2].name
