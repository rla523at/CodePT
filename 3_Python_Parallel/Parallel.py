import os, time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def heavy_for(iters: int, seed: int) -> int:
    x = seed & 0xFFFFFFFF

    acc = 0
    for i in range(iters):
        x = (x * 1664525 + 1013904223) & 0xFFFFFFFF
        acc ^= (x * ((i << 1) | 1)) & 0xFFFFFFFF
        acc = ((acc << 7) | (acc >> 25)) & 0xFFFFFFFF
    return acc

def run_forloop_benchmark(num_repeat):

    # worker 의 수가 논리 core 수와 같을 때
    workers = os.cpu_count()

    # # worker 의 수가 physical core 수와 같을 때
    # workers = 4

    print("num_worker:", workers)

    num_tasks = 12

    seeds = [0x9E3779B9 + i * 2654435761 for i in range(num_tasks)]
    iters = [num_repeat]*num_tasks

    def stamp(msg, t0):
        print(f"{msg} {time.perf_counter()-t0:7.5f}s")

    # 1) baseline
    t0 = time.perf_counter()
    base_res = [heavy_for(num_repeat, s) for s in seeds]
    stamp("[CPU] baseline     ", t0)
    print("      sample:", base_res[:4])

    # 2) threads (GIL로 인해 보통 이득이 적거나 역전)
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        thr_res = list(ex.map(heavy_for, iters, seeds))
    stamp("[CPU] threads      ", t0)
    print("      sample:", thr_res[:4])

    # 3) processes (프로세스별 GIL → 진짜 병렬)
    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        pro_res = list(ex.map(heavy_for, iters, seeds))
    stamp("[CPU] processes    ", t0)
    print("      sample:", pro_res[:4])

    # 4) processes without 초기화 비용
    # ProcessPoolExecutor(max_workers=...)는 내부적으로 워커 스폰을 시작하지만, 생성자가 워커 준비 완료까지 기다려주지 않는다.
    pool = ProcessPoolExecutor(max_workers=workers)

    # 첫 작업 제출 시 본격적으로 완료되는 사항들
    # - 부모–자식 간 파이프/소켓 핸드셰이크 안정화
    # - 작업 직렬화/역직렬화(피클) 경로 확인
    # - 자식 프로세스의 모듈 임포트/런타임 초기화
    # pool.map(...)은 “게으른 이터레이터”를 돌려주기 때문에 list 로 실체화함    
    list(pool.map(int, [0]*workers))

    t0 = time.perf_counter()
    pro_res = list(pool.map(heavy_for, iters, seeds))
    stamp("[CPU] processesOpt ", t0)
    print("      sample:", pro_res[:4])
    pool.shutdown()

    pool = ProcessPoolExecutor(max_workers=workers)
    t0 = time.perf_counter()
    pro_res = list(pool.map(heavy_for, iters, seeds))
    stamp("[CPU] processesOpt ", t0)
    print("      sample:", pro_res[:4])
    pool.shutdown()

if __name__ == "__main__":
    run_forloop_benchmark( num_repeat=100_000)
