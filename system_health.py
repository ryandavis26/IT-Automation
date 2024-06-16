import shutil
import psutil



def check_disk_usage(disk):
    du = shutil.disk_usage("/")
    free_space = (du.free/du.total) * 100
    return free_space > 20


def check_cpu_usage():
    cpu_usage = psutil.cpu_percent(1.0)
    return cpu_usage < 75


if __name__ == '__main__':
    if not check_disk_usage("/") or not check_cpu_usage():
        print("System may not be healthy")
    else:
        print("System  cpu and disk usage is healthy")
