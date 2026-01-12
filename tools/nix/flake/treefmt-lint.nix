{ pkgs, ... }:
{
  # Used to find the project root
  projectRootFile = ".git/config";

  settings.global.excludes = [
    "external/*"
    "tools/scripts/generate-spec.py"
  ];

  # Python
  programs.ruff-check.enable = true;

  # Shell
  programs.shellcheck.enable = true;

  # Typos.
  programs.typos.enable = false;
}
