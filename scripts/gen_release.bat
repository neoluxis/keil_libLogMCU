@echo off
chcp 65001

set "target=libLogMCU"

if exist "./%target%/" (
    echo 找到 %target% 在当前目录，开始打包...
) else if exist "../%target%/" (
    echo 找到 %target% 在上级目录，开始打包...
    cd ..
) else (
    echo 错误：未能在 ./ 或 ../ 找到 %target% 文件夹
)

echo Zipping sources ans headers...
tar -a -c -f libLogMCU_src.zip -C ./libLogMCU Library

echo Zipping lib and headers...
tar -a -c -f libLogMCU_bin.zip -C ./libLogMCU_tests Library

pause