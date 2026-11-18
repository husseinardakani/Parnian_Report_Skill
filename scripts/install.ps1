$Manager = Join-Path $PSScriptRoot 'manage.py'
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $Manager @args
} else {
    & python $Manager @args
}
exit $LASTEXITCODE
