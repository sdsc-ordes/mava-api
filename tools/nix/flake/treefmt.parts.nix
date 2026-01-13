{ inputs, ... }:
{
  perSystem =
    { pkgs, ... }:
    let
      treefmtEval = inputs.treefmt-nix.lib.evalModule pkgs ./treefmt.nix;
      treefmt = treefmtEval.config.build.wrapper;

      treefmtEvalLint = inputs.treefmt-nix.lib.evalModule pkgs ./treefmt-lint.nix;
      treefmt-lint = treefmtEvalLint.config.build.wrapper;
    in
    {
      formatter = treefmt;

      packages.treefmt = treefmt;

      # Wrap over bash due to the executable in `treefmt`
      # having the same name.
      packages.treefmt-lint =
        pkgs.writeShellScriptBin "treefmt-lint"
          # bash
          ''
            echo "Running 'treefmt' linting configuration."
            ${treefmt-lint}/bin/treefmt "$@"
          '';
    };
}
