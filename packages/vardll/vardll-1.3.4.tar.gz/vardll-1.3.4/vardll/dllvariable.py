import ctypes

class DLLvar:
    def import_file(self, full_path):
        try:
            dll_module = ctypes.CDLL(full_path)
            return dll_module
        except OSError as e:
            raise FileNotFoundError(f"Could not find or load DLL file: {full_path}") from e

dll = DLLvar()
