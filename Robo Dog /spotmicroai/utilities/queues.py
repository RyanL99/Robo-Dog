
import multiprocessing as mp
def get_queues(names): return {name: mp.Queue() for name in names}
