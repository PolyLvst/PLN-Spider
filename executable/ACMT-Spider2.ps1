.\venv\Scripts\activate
py main-acmt.py -p 2
$exitCode = $LASTEXITCODE
if ($exitCode -gt 0) {
    echo Error
    py warning_sound.py
}