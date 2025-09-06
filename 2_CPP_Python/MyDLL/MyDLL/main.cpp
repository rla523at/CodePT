// extern "C" :Name Mangling 방지
// __declspec(dllexport) : DLL Export Table 에 올려 외부에서 호출 가능하게 함

extern "C" __declspec(dllexport) double step(double x)
{
  return 3.0 * x + 1.0;
}
