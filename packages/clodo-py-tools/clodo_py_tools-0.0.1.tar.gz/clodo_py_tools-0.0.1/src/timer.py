def timer(function):
    import functools
    @functools.wraps(function)
    def wrapper_timer(*args, **kwargs):
        import time
        start_time = time.perf_counter()
        value = function(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        return f"Finished {function.__name__}() in {run_time:.4f} secs"
    return wrapper_timer

def benchmark(function):
    import functools
    @functools.wraps(function)
    def wrapper_benchmark(*args, **kwargs):
        import time

        run_times = []

        for iteration in range(1,1000):
            start_time = time.perf_counter()
            value = function(*args, **kwargs)
            end_time = time.perf_counter()
            run_time = end_time - start_time
            print(f"Finished {function.__name__}() in {run_time:.4f} secs")
            run_times.append(run_time) 

        mean_run_time = sum(run_times)/len(run_times) 

        print(f"Run time - Mean: {mean_run_time:.4f}")

    return wrapper_benchmark