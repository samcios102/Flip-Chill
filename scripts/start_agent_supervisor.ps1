param(
  [string]$BotCommand = $env:FLIPPCHILL_BOT_COMMAND,
  [int]$IntervalSeconds = 15
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

if (-not $BotCommand) {
  Write-Host 'FLIPPCHILL_BOT_COMMAND is not set.' -ForegroundColor Yellow
  Write-Host 'Set it to the command used to launch your local OpenCode/bot. The template may use {prompt_file}, {agent}, {task_id}.'
  Write-Host 'The dispatcher will still create AI_SYNC/BOT_INBOX.md, but automatic launch requires the command.'
} else {
  $env:FLIPPCHILL_BOT_COMMAND = $BotCommand
  Write-Host "Bot command configured. Starting FlippChill AI_SYNC watcher..." -ForegroundColor Green
}

python scripts/agent_dispatch.py --watch --interval $IntervalSeconds
