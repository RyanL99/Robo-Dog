import multiprocessing as mp
def make(names): return {n:mp.Queue() for n in names}
