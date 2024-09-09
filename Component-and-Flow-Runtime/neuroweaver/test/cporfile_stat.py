# python3.8 -m cProfile -o b1stats benchmark1.py
import pstats
from pstats import SortKey
from scalene import scalene_profiler
scalene_profiler.start()
p = pstats.Stats('b1_ppruntime')
#p.sort_stats(SortKey.CUMULATIVE).print_stats(10)
#p.sort_stats('tottime').print_stats(50)
p.sort_stats('tottime').print_callers(50)
#p.strip_dirs().sort_stats(-1).print_stats()
scalene_profiler.stop()
#print(scalene_profiler.__dict__)

