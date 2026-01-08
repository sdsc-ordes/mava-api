{ inputs, ... }:
{
  perSystem =
    { pkgs, ... }:
    let
      treefmtEval = inputs.treefmt-nix.lib.evalModule pkgs ./treefmt.nix;
      treefmt = treefmtEval.config.build.wrapper;

      ruff = pkgs.python3.pkgs.ruff;
    in
    {
      packages.treefmt = treefmt;
      packages.ruff = ruff;
      formatter = treefmt;
    };
}
