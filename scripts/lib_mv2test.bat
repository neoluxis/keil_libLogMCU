echo off

echo Cleaning old lib fils in testing project...
:: Remove old headers
rd /s /q "..\..\libABC_tests\Library\inc"
:: Remove old lib
del /f /q "..\..\libABC_tests\Library\libABC.lib"

echo Moving .lib file£¨libABC.lib£©
copy /y "build\libABC.lib" "..\..\libABC_tests\Library\"

echo Moving headers
xcopy /q "..\Library\inc" "..\..\libABC_tests\Library\inc\" /e /i /h /y

echo Finish