// extern "C" :Name Mangling ����
// __declspec(dllexport) : DLL Export Table �� �÷� �ܺο��� ȣ�� �����ϰ� ��

extern "C" __declspec(dllexport) double step(double x)
{
  return 3.0 * x + 1.0;
}
