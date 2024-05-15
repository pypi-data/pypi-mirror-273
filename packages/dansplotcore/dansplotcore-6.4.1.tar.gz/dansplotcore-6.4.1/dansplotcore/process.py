import math

def avg(x):
    return sum(x) / len(x)

def bucket(l, bucket_count=None):
    if bucket_count == None:
        bucket_count = math.ceil(len(l) / 10)
    data_min = min(l)
    data_max = max(l)
    data_range = data_max - data_min
    bucket_size = data_range / bucket_count * 1.001
    buckets = [0 for _ in range(bucket_count)]
    for i in l:
        index = math.floor((i - data_min) / bucket_size)
        buckets[index] += 1
    return [(data_min + i * bucket_size, v) for i, v in enumerate(buckets)]

def contours(points, *, n=5, ticks=1000, spread=100, plot=None):
    '''
    Take in a list of (x, y) points and spit out a list of (x, *y_avg_i) for i in [0, n).
    A window is slid from min(x) to max(x) and at each spot, n trimmed averages are taken.
    y_avg_0 is the minimum value in the window.
    y_avg_m is the average of the window for odd n, m = (n-1)/2
    y_avg_h is the high-half trimmed average of the window, h ~= n * 3 / 4
    y_avg_M is the maximum value in the window, M = n-1

    ticks says how many windows to evaluate.
    spread says how wide the windows should be. 1 means no overlap between windows, 0 means the windows have no width, 2 means each window overlaps half of each neighbor.

    If a plot is passed in, the contours are added to it.
    '''
    x_min = min(i[0] for i in points)
    x_max = max(i[0] for i in points)
    x_range = x_max - x_min
    x_scale = x_range / ticks
    x_spread = x_scale * spread / 2
    lines = []
    for tick in range(ticks):
        x = x_min + tick * x_scale
        window_min = x - x_spread
        window_max = x + x_spread
        bucket = sorted(y for (x, y) in points if window_min <= x < window_max)
        if not bucket: continue
        avgs = []
        for i in range(0, n):
            a = int((len(bucket) - 1) * (i / (n-1) * 2 - 1))
            b = a + len(bucket)
            a = max(a, 0)
            b = min(b, len(bucket))
            avgs.append(avg(bucket[a:b]))
        lines.append((x, *avgs))
    if plot:
        for (xi, *yi), (xf, *yf) in zip(lines, lines[1:]):
            for i in range(n):
                m = (n-1) / 2
                plot.line(xi, yi[i], xf, yf[i], r=0, g=1 - abs(i - m) / m)
    return lines
