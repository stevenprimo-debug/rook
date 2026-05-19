# drift-linter.ps1
# Fires on PreToolUse for Edit|Write|NotebookEdit tools.
# Purpose: surface project-context awareness BEFORE Claude writes/edits a file.
# Catches the failure mode where Claude silently switches project context mid-response.
#
# Outputs to stderr (visible to Claude as feedback). Does NOT block (exit 0).
# V1 = observation. V2 (later) could block on confirmed violations.

$raw = [Console]::In.ReadToEnd()
try { $data = $raw | ConvertFrom-Json } catch { $data = $null }

$tool = if ($data.tool_name) { $data.tool_name } else { "" }
$path = ""
if ($data.tool_input.file_path) { $path = $data.tool_input.file_path }
elseif ($data.tool_input.notebook_path) { $path = $data.tool_input.notebook_path }

# Only lint Edit|Write|NotebookEdit (state-changing tools)
$lintTargets = @("Edit", "Write", "NotebookEdit")
if (-not ($lintTargets -contains $tool)) {
    exit 0
}

# Determine project/dept context from path
$context = "UNKNOWN"
$ctxDetail = ""
if ($path -match "DEPARTMENTS\\([^\\]+)") {
    $dept = $Matches[1]
    $context = "DEPT: $dept"
    if ($path -match "DEPARTMENTS\\$dept\\COMPANIES\\([^\\]+)") {
        $client = $Matches[1]
        $ctxDetail = "  (client project: $client)"
    } elseif ($path -match "DEPARTMENTS\\$dept\\skills\\([^\\]+)") {
        $skill = $Matches[1]
        $ctxDetail = "  (skill: $skill)"
    } elseif ($path -match "DEPARTMENTS\\$dept\\memory") {
        $ctxDetail = "  (memory entry)"
    }
} elseif ($path -match "CLAUDE CODE\\MEMORY") {
    $context = "ROOT MEMORY"
} elseif ($path -match "\\\.claude\\hooks\\") {
    $context = "HARNESS HOOK"
    $ctxDetail = "  (this changes the harness itself -- be sure)"
} elseif ($path -match "\\\.claude\\settings\\.json|\\\.claude\\settings\.json") {
    $context = "HARNESS CONFIG"
    $ctxDetail = "  (this changes Claude Code config)"
} elseif ($path -match "SKILLS\\([^\\]+)") {
    $skill = $Matches[1]
    $context = "PROJECT SKILL: $skill"
} elseif ($path -match "CLAUDE\.md") {
    $context = "INSTRUCTION FILE"
    $ctxDetail = "  (modifies Claude's behavior in this scope)"
}

# Surface to stderr (Claude sees as system feedback)
$out = @(
    "",
    "[drift-linter] $tool -> $context",
    $ctxDetail,
    "[drift-linter] Confirm this matches the project context the operator asked about.",
    "[drift-linter] If you pivoted from a different context (e.g. PrimoLabs to a client project, or vice versa), you should have named that pivot explicitly in your last response."
)

# Filter empty lines
$out | Where-Object { $_ -ne "" } | ForEach-Object { [Console]::Error.WriteLine($_) }

exit 0
