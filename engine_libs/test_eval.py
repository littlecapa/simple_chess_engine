from __future__ import print_function

from eval import Eval as e

evaluator = e()

score = evaluator.get_score(b"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
print("Score = ", score)