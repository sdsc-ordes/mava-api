{ pkgs, ... }:
{
  # Used to find the project root
  projectRootFile = ".git/config";

  settings.global.excludes = [
    "external/*"
    "tools/scripts/generate-spec.py"
  ];

  # Markdown, JSON, YAML, etc.
  programs.prettier.enable = true;

  # Python
  programs.ruff-format.enable = true;

  # Shell.
  programs.shfmt = {
    enable = true;
    indent_size = 4;
  };

  programs.gofmt.enable = true;
  programs.goimports.enable = true;

  # Lua.
  programs.stylua.enable = true;

  # Nix.
  programs.nixfmt.enable = true;
}
