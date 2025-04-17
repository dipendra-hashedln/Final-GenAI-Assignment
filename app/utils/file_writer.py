# app/utils/file_writer.py

import os

def write_module_files(file_map: dict, base: str):
    """
    Writes each code string to its corresponding file under `base`.
    file_map keys are relative paths like 'app/routes/user.py'
    """
    for rel_path, code in file_map.items():
        full = os.path.join(base, rel_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(code)


