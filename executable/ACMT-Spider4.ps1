.\venv\Scripts\activate
py main-acmt.py -p 4
$exitCode = $LASTEXITCODE
if ($exitCode -gt 0) {
    echo Error
    py warning_sound.py
}