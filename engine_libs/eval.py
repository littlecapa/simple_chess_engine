from ctypes import *

class Eval():

    def __init__(self):
        self.nnue = cdll.LoadLibrary("engine_libs/libnnueprobe.so")
        self.nnue.nnue_init(b"engine_libs/nn-04cf2b4ed1da.nnue")
        print("Init ok")

    def get_score(self, fen):
        return self.nnue.nnue_evaluate_fen(bytes(fen, encoding='utf-8'))