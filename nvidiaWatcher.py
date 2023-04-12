from pynvml import *
import time
import sys



while True:
    nvmlInit()
    #查看设备
    deviceCount = nvmlDeviceGetCount()
    for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        print("GPU", i, ":", nvmlDeviceGetName(handle))

    #查看显存、温度、风扇、电源
    handle = nvmlDeviceGetHandleByIndex(0)
    info = nvmlDeviceGetMemoryInfo(handle)
    print("Memory Total: %d MB." % (info.total // (1024 * 1024)))
    print("Memory Free: %d MB." % (info.free // (1024 * 1024)))
    print("Memory Used: %d MB." % (info.used // (1024 * 1024)))

    print("Temperature is %d C"%nvmlDeviceGetTemperature(handle,0))
    print("Fan speed is ", nvmlDeviceGetFanSpeed(handle))
    print("Power ststus", nvmlDeviceGetPowerState(handle))
    nvmlShutdown()

    time.sleep(1)
