import ctypes
from ctypes import c_double

# cdecl DLL이면 CDLL 사용 (기본 규약)
lib = ctypes.CDLL("./MyDLL.dll")

# 시그니처 지정: double step(double)
lib.step.argtypes = [c_double]
lib.step.restype  = c_double

def iterate(initial_input, steps):

    # ctypes가 argtypes에 맞춰 c_double로 자동 변환해준다. 
    # c_double은 “C에 넘길 때 쓰는 ctypes 타입”이지, 파이썬 코드 안에서 연산용 변수 타입으로 쓸 필요는 없다.
    dll_input = float(initial_input)
    
    for i in range(steps):
      # C++ DLL 호출
      # dll_output 타입은 파이썬 float 이다. ctypes가 C의 double 반환값을 파이썬 기본형(float) 으로 자동 변환한다.
      dll_output = lib.step(dll_input)         

      # 후처리
      next_dll_input = 0.5 * (dll_input + dll_output)
      print(f"[{i+1}] dll_input={dll_input:.6f} -> dll_output={dll_output:.6f} -> x'={next_dll_input:.6f}")
      dll_input = next_dll_input
    return dll_input

if __name__ == "__main__":
    final_x = iterate(initial_input=2.0, steps=6)
    print(f"\nFinal x = {final_x:.6f}")
