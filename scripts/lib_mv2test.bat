@echo off

echo Cleaning old lib fils in testing project...
:: Remove old headers
rd /s /q "..\..\libLogMCU_tests\Library\inc"
:: Remove old lib
del /f /q "..\..\libLogMCU_tests\Library\libLogMCU.lib"

echo Moving .lib file 
copy /y "build\libLogMCU.lib" "..\..\libLogMCU_tests\Library\"

echo Moving headers
xcopy /q "..\Library\inc" "..\..\libLogMCU_tests\Library\inc\" /e /i /h /y

echo Finish