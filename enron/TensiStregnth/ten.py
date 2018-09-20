from subprocess import *

def stressAnalysis(text):
    process = Popen(['java', '-jar', './TensiStrengthMain.jar', 'sentidata', './TensiStrength_Data/', 'explain', "text",
                     text, "urlencoded", "mood", "0"], stdout=PIPE, stderr=PIPE)
    line = process.stdout.readline().decode("utf-8")
    print(line)
    
    ret = line.split("+")
    relax_level = ret[0]
    stress_level = ret[1]

    return (relax_level,stress_level)

ret = stressAnalysis("This is a test,adf")
print(ret)



