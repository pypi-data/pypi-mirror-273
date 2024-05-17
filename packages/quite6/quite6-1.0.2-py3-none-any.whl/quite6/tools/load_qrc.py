import os
import st
import sys
import subprocess
import PySide6

if sys.platform == 'darwin':
    pyside6_path = os.path.dirname(sys.executable)
    rcc_path = os.path.join(pyside6_path, 'pyside6-rcc')
    if not os.path.exists(rcc_path):
        print(f'PySide6 Resource Compiler (pyside6-rcc) Not Found in platform {rcc_path}!')
elif sys.platform == 'win32':
    pyside6_path = os.path.dirname(PySide6.__file__)
    rcc_path = os.path.join(pyside6_path, 'pySide6-rcc.exe')
    if not os.path.exists(rcc_path):
        rcc_path = 'PySide6-rcc.exe'
    if not os.path.exists(rcc_path):
        print('PySide6 Resource Compiler (PySide6-rcc.exe) Not Found!')
else:
    print(f"Unsupported platform {sys.platform} for pyside6-rcc")


@st.make_cache
def compile_qrc(filename):
    command = rcc_path + ' -g python ' + filename
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, error) = p.communicate()
    p.wait()
    if p.returncode != 0:
        raise IOError(f'There was an error compiling the .qrc file {filename}: {error}')
    output = output.decode()
    return output


def load_qrc(filename):
    code = compile_qrc(filename)
    st.run(code)
