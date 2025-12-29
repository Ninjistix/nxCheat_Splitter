@echo off
REM ========================================
REM nxCheat_Splitter Build Script
REM Builds a standalone nxCheat_Splitter.exe from src/*.pyw or src/*.py using PyInstaller
REM Works even if the main folder is renamed
REM ========================================

REM Get the directory of this batch file
SET ROOT_DIR=%~dp0

REM Set paths relative to the batch file
SET SRC_DIR=%ROOT_DIR%src
SET ASSETS_DIR=%ROOT_DIR%assets
SET DIST_DIR=%ROOT_DIR%dist
SET BUILD_DIR=%ROOT_DIR%build

REM Find the main Python script in src (prioritize .pyw)
FOR %%F IN ("%SRC_DIR%\*.pyw") DO SET MAIN_SCRIPT=%%F
IF NOT DEFINED MAIN_SCRIPT (
    FOR %%F IN ("%SRC_DIR%\*.py") DO SET MAIN_SCRIPT=%%F
)

IF NOT DEFINED MAIN_SCRIPT (
    ECHO ERROR: No Python script found in %SRC_DIR%.
    PAUSE
    EXIT /B 1
)

REM Find icon in assets (prioritize .ico)
FOR %%F IN ("%ASSETS_DIR%\*.ico") DO SET ICON_FILE=%%F
IF NOT DEFINED ICON_FILE (
    ECHO WARNING: No .ico file found in %ASSETS_DIR%. Using default icon.
    SET ICON_OPTION=
) ELSE (
    SET ICON_OPTION=--icon="%ICON_FILE%"
)

REM Clean previous builds
IF EXIST "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
IF EXIST "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"

REM Build the .exe as nxCheat_Splitter.exe
pyinstaller --noconsole --windowed --onefile %ICON_OPTION% --add-data "%ASSETS_DIR%";assets -n nxCheat_Splitter "%MAIN_SCRIPT%"

REM Delete the .spec file to keep folder clean
IF EXIST "%ROOT_DIR%nxCheat_Splitter.spec" del "%ROOT_DIR%nxCheat_Splitter.spec"

REM Delete the build folder to keep project clean
IF EXIST "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"

REM Done
ECHO Build complete. The .exe is in %DIST_DIR%\nxCheat_Splitter.exe
PAUSE
