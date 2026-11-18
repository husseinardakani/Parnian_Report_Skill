# Parnian Enterprise Reporting

`parnian-enterprise-reporting` coordinates requirements, analytics, report architecture, approval, and validation for Parnian projects. It routes to available specialists for Power BI modeling and authoring, SQL/data analysis, UI/UX, product requirements, visualization, PDF, and spreadsheets.

## Codex CLI and VS Code

Check out a reviewed revision of this repository. The installers require Python 3.9+ and, with Microsoft skills enabled, Git and GitHub access. Run the commands from the checkout. The Windows example uses PowerShell and the Codex extension with a local Windows workspace. For WSL or a remote extension host, run the installer on that host.

```bash
./scripts/install.sh validate
./scripts/install.sh install --with-upstream
./scripts/install.sh status
```

```powershell
.\scripts\install.ps1 validate
.\scripts\install.ps1 install --with-upstream
.\scripts\install.ps1 status
```

Omit `--with-upstream` to install the central skill alone. The user-scoped bundle lives at `~/.agents/skills/parnian-reporting` (Windows `%USERPROFILE%\.agents\skills\parnian-reporting`). The bundle preserves Microsoft's relative reference paths and license. A matching upstream skill already present in the selected root is reused. Review other configured skill scopes for same-name skills when setting up a new environment. `--skills-root` selects an explicit alternative root, including for isolated testing. Codex discovery requires that root to be in a recognized scope.

Start a new Codex session or reload the IDE if the skill list is stale. Check `/skills` where supported, or run `python scripts/check-discovery.py --with-upstream` with the Codex CLI on PATH. This checks actual discovery in two unrelated temporary directories. Use the same host and user as the extension.

## Codex Cloud

Select this repository and the reviewed branch in Codex Cloud. The repo-local `.agents/skills` directory supplies the central skill inside this checkout. Other Parnian repositories can incorporate the same central skill directory from a reviewed revision to get repository-local discovery, or use a managed Cloud environment setup script to install the bundle for the environment user. Fetch the reviewed checkout during setup and run `./scripts/install.sh install --with-upstream` where user-scope writes and GitHub access are available. Keep repository-local and user-scoped copies in sync or choose one scope to avoid duplicate names in the same session. Cloud user-scope installation applies to that environment and needs to be provisioned again for new environments. It does not propagate to a Windows machine or unrelated Cloud environment.

## Update and uninstall

Check out the new reviewed revision and run `update` through the same wrapper. Include `--with-upstream` to retain the pinned Microsoft skills in the replacement bundle. Run `status` and verify Codex discovery again. For uninstall, run the same wrapper with `uninstall` and the same root. A managed-file change or an unmanaged bundle causes the installer to stop. Preserve any local edits before restoring the installed files or moving the bundle aside. If an interrupted operation leaves the named lock directory in the skill root, confirm no installer is running before removing that lock. The workflow does not change any Codex or MCP configuration.

## Usage

Try “Design a Parnian Blazor dashboard for monthly order volume with a Jalali date filter and an Excel export.” This matches the skill description without an explicit invocation. Expect requirements discovery, a summary of selected skills, a KPI definition or a question about its grain, and a proposal for approval before implementation. You can also invoke `$parnian-enterprise-reporting` explicitly.

See [routing](.agents/skills/parnian-enterprise-reporting/references/routing.md), [dependency pins](dependencies.json), and the [setup audit and test record](SETUP.md).
