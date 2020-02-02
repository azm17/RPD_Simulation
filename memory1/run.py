import subprocess

# subprocess.run(["./a.out"])

# cmd = ["./a.out"] + ["0","0","0","0","0"]
cmd = ["a.exe"] + ["0","0","0","0","0"]
proc = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
# print(proc.stdout.decode("utf8").split('\n')[:-1])

x_list=[]; y_list=[]
for l in proc.stdout.decode("utf8").split('\n')[:-1]:
    tmp = l.split(',')
    x_list.append(float(tmp[0]))
    y_list.append(float(tmp[1]))
print(x_list[0], y_list[0])
