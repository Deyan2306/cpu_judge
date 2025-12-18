import multiprocessing
import os
import signal
import sys
import time

def stress_core(core_index):
    print(f"[Core {core_index}] Stressing Process ID: {os.getpid()}")

    val = 1.1
    try:
        while True:.
            val = (val * 1.000001) / 1.000001
            
            if val > 100:
                val = 1.1
    except KeyboardInterrupt:
        pass

def start_load():
    cpu_count = multiprocessing.cpu_count()
    print(f"--- CPU STRESS TEST ---")
    print(f"Detected {cpu_count} cores.")
    print(f"Targeting all cores... Press Ctrl+C to stop.")

    processes = []
    for i in range(cpu_count):
        p = multiprocessing.Process(target=stress_core, args=(i,))
        p.daemon = True 
        p.start()
        processes.append(p)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Stopping load... Cleaning up processes.")
        for p in processes:
            p.terminate()
            p.join()
        print("All processes stopped. Cores should be cooling down now.")

if __name__ == "__main__":
    start_load()
