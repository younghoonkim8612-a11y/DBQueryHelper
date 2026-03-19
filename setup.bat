@echo off
echo ============================================
echo   DB Query Helper - Setup
echo ============================================
echo.

:: Python 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python이 설치되어 있지 않습니다.
    echo Python 3.11 이상을 설치하세요: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Claude Code CLI 확인
claude --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Claude Code CLI가 설치되어 있지 않습니다.
    echo 설치: npm install -g @anthropic-ai/claude-code
    echo Max 구독 로그인 필요: claude login
    echo.
)

:: 가상환경 생성
if not exist "venv" (
    echo [1/3] 가상환경 생성 중...
    python -m venv venv
) else (
    echo [1/3] 가상환경 이미 존재
)

:: 패키지 설치
echo [2/3] 패키지 설치 중...
venv\Scripts\pip.exe install -r requirements.txt -q

:: connections.json 확인
if not exist "connections.json" (
    echo [3/3] connections.json 파일이 없습니다.
    echo 연결 관리 페이지에서 DB 연결 정보를 등록하세요.
) else (
    echo [3/3] connections.json 확인 완료
)

echo.
echo ============================================
echo   설치 완료!
echo ============================================
echo.
echo 실행 방법:
echo   run.bat
echo.
pause
