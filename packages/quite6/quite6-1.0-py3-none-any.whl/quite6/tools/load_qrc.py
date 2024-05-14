import os
import st
import subprocess
import PySide6

PySide6_path = os.path.dirname(PySide6.__file__)
rcc_path = os.path.join(PySide6_path, 'PySide6-rcc.exe')
if not os.path.exists(rcc_path):
    rcc_path = 'PySide6-rcc.exe'
if not os.path.exists(rcc_path):
    print('PySide6 Resource Compiler (PySide6-rcc.exe) Not Found!')


@st.make_cache
def compile_qrc(filename):
    command = rcc_path + ' -py3 ' + filename
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, _) = p.communicate()
    p.wait()
    output = output.decode()
    return output


def load_qrc(filename):
    code = compile_qrc(filename)
    st.run(code)
