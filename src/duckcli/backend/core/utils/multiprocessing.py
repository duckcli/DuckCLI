import time

from multiprocessing.pool import ThreadPool


def multi_processing(pool_limit, wrapper_func, func_values):
    """ """

    start = time.time()
    pool = ThreadPool(pool_limit)
    results = pool.map(wrapper_func, func_values)
    pool.close()
    pool.join()
    end = time.time()
    print(end - start)
    return results
