$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Backend = Join-Path $Root "backend"

if (-not $env:OPEN_PIT_WALL_HOME) {
  $env:OPEN_PIT_WALL_HOME = Join-Path $Root "data\replay"
}

Set-Location $Backend
python -m open_pit_wall @args
