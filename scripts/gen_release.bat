@echo off
chcp 65001

set "target=libABC"

if exist "./%target%/" (
    echo 找到 %target% 在当前目录，开始打包...
) else if exist "../%target%/" (
    echo 找到 %target% 在上级目录，开始打包...
    cd ..
) else (
    echo 错误：未能在 ./ 或 ../ 找到 %target% 文件夹
)

echo Zipping sources ans headers...
tar -a -c -f libABC_src.zip -C ./libABC Library

echo Zipping lib and headers...
tar -a -c -f libABC_bin.zip -C ./libABC_tests Library

pause