from quick_fuoss import compute_kd
import time

start_time = time.time()

assert (compute_kd("potassium", "chloride", 20) - 0.0084) < 0.0001
assert (compute_kd("sodium", "chloride", 20) - 0.0055) < 0.0001
assert (compute_kd("static/quinolinium.xyz", "static/tetraphenylborate.xyz", 20) - 0.02196) < 0.0001
assert (compute_kd("static/quinolinium.xyz", "chloride", 20) - 0.01082) < 0.0001

assert (compute_kd("sodium", "chloride", 10) - 0.000005) < 0.00001
assert (compute_kd("sodium", "chloride", 40) - 0.18644) < 0.0001
assert (compute_kd("sodium", "chloride", 20, 400) - 0.03335) < 0.0001

assert (compute_kd("tetraisoamylammonium", "nitrate", 8.5) - 0.000049) < 0.0001
assert (compute_kd("tetraisoamylammonium", "nitrate", 11.9) - 0.0009) < 0.0001

end_time = time.time()

print(f"All tests successful! (9 tests run in {end_time-start_time:.2f} seconds)")
