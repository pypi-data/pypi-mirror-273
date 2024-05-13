# DEEPGPU Package Build

## For SLA
1. edit version and deepytorch commitid in setup-sla.py
2. build package
```
./build-sla.sh
```
3. upload to oss://aiacc/deepgpu/

## For Release
1. edit version in setup.py
2. build package
```
./build.sh
```
3. upload to https://pypi.org/project/deepgpu/