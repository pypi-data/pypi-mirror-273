import setuptools
import subprocess
from setuptools.command.install import install
import os

NAME="deepgpu"
DEEPGPU_VERSION = "2.1.0"
DEEPYTORCH_PKG_VERSION = DEEPGPU_VERSION # same as DEEPGPU version so far
support_os_list = ['ubuntu', 'centos', 'alinux'] # add version later
support_pytorch_version = ['1.10', '1.11', '1.12', '1.13', '2.0', '2.1']
support_cuda_version = ['11.1', '11.3', '11.6', '11.7', '11.8', '12.1', '12.3']
support_python_version = ['38', '39', '310', '311']

_root_path_deepgpu = "https://mirrors.aliyun.com/deepgpu/"
_root_path_deepytorch = f"{_root_path_deepgpu}/deepytorch/{DEEPYTORCH_PKG_VERSION}/"
_temp_path = f"{os.environ['HOME']}/.deepgpu/"
_temp_log = f"{_temp_path}/log"

tsinghua_source = "https://pypi.tuna.tsinghua.edu.cn/simple"


class PostInstallCommand(install):

    def get_environment(self):
        os_name = None
        python_version = None
        framework = None
        cuda_version = None

        def get_os_name():
            # return 'debian'
            distro_install = ["pip3", "install", "--no-deps", "--quiet", "distro"]
            distro_install_res = subprocess.run(distro_install)
            if distro_install_res.returncode != 0:
                os.system(f'echo "Install distro failed! {distro_install_res.stderr}" >> {_temp_log} ')
            import distro
            return distro.id()

        def get_python_version():
            # return '3.7.13'
            import platform
            return platform.python_version()

        def get_python_abi():
            # return 'm'
            import platform
            return platform.sys.abiflags

        def get_framework():
            # return {'torch': '1.6'} or {'torch': '1.6.0a0'}
            try:
                import torch
                torch_version = torch.__version__.split('+')[0]
                torch_major_and_minor_version = torch_version.rsplit(".", 1)[0]
                torch_patch = torch_version.split('.')[2]
                if torch_patch[-2:] == 'a0':
                    # ngc
                    framework_version = torch_version
                else:
                    framework_version = torch_major_and_minor_version
                return {"torch": framework_version}
            except:
                return None

        def get_cuda_version():
            # return '10.1'
            try:
                import torch
                return torch.version.cuda
            except:
                return None

        os_name = get_os_name()
        python_version = get_python_version()
        python_abi = get_python_abi()
        framework = get_framework()
        cuda_version = get_cuda_version()
        assert framework is not None, \
            f"Please install PyTorch before installing the {NAME}."
        return os_name, python_version, python_abi, framework, cuda_version

    def check_deepgpu_version(self, os_name, python_version, cuda_version,
                              framework_type, framework_version):
        """
        deepgpu support version following Pytorch.
        Ref: https://download.pytorch.org/whl/torch/

        Examples:
            torch-1.9.0+cu102-cp36-cp36m-linux_x86_64.whl

        """
        supported = True
        if python_version not in support_python_version:
            supported = False
        # for ngc
        if framework_version[-2:] != 'a0':
            if os_name.lower() not in support_os_list:
                supported = False
                assert supported == True, \
                    f"{NAME}-{DEEPGPU_VERSION} installed failed for not testing on this os: {os_name} "
            if cuda_version not in support_cuda_version:
                supported = False
            if framework_version not in support_pytorch_version:
                supported = False
        assert supported == True, \
            f"{NAME}-{DEEPGPU_VERSION} installed failed for not supporting torch with version: " \
            f"{framework_type}-{framework_version}+cu{cuda_version}-cp{python_version}"
        os.system(f'echo "check deepgpu-version successed!" >> {_temp_log} ')

    def run(self):
        # get env
        os_name, py, py_abi, dl, cu = self.get_environment()

        # set env
        if not os.path.exists(f'{_temp_path}'):
            os.system(f'mkdir -p {_temp_path}')
        os.system(f'echo py:{py}, py_abi:{py_abi}, dl:{dl}, cu:{cu}  > {_temp_log}')
        python_version = "".join(py.split('.')[:2])
        cuda_version = cu
        framework_type = list(dl.keys())[0]
        framework_version = list(dl.values())[0]
        self.check_deepgpu_version(os_name,
                                   python_version,
                                   cuda_version,
                                   framework_type,
                                   framework_version)

        if framework_version[-2:] == 'a0':
            framework_version = 'any'
            cuda_version = 'any'
        # install deepytorch
        pkg = f"{_root_path_deepytorch}" \
            f"deepytorch-{DEEPYTORCH_PKG_VERSION}+{framework_type}{framework_version}" \
            f"cuda{cuda_version}-cp{python_version}-cp{python_version}{py_abi}-" \
            f"linux_x86_64.whl"
        os.system(f'echo "Install: {pkg}" >> {_temp_log}')
        cmd = ["pip3", "install", "--no-cache-dir", "--force-reinstall",
               "--quiet", pkg, "-i",  tsinghua_source]
        res = subprocess.run(cmd)
        if res.returncode == 0:
            os.system(f'echo "Install success!" >> {_temp_log}')
        else:
            count = 3 # retry
            while(count != 0):
                res = subprocess.run(cmd)
                if res.returncode == 0:
                    os.system(f'echo "Install success!" >> {_temp_log}')
                    break
                else:
                    count -= 1
            if res.returncode != 0:
                os.system(f'echo "Install failed! {res.stderr}" >> {_temp_log}')

        install.run(self)


setuptools.setup(
    name=NAME,
    version=DEEPGPU_VERSION,
    description=("DEEPGPU is a toolset for AI training acceleration on Alibaba Cloud."),
    author="Alibaba Cloud",
    license="Copyright (C) Alibaba Group Holding Limited",
    keywords="Distributed, Deep Learning, Communication, NCCL, Pytorch, Tensorflow",
    url="https://www.aliyun.com",
    long_description=(f"It includes a distributed training framework plugin for PyTorch, "
        "and a nccl runtime plugin for many deep learning framworks including "
        "PyTorch, TensorFlow and .etc. This project aims to make the distributed "
        "training as easy as possible and as fast as possible on Alibaba Cloud."),
    packages=setuptools.find_packages(),
    include_package_data=True,
    cmdclass = { 'install': PostInstallCommand },
    python_requires='>=3.8'
)
