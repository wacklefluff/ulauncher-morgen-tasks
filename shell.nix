{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    # Python environment
    python3
    python3Packages.requests

    # Dev tools
    python3Packages.black
    python3Packages.pylint
    python3Packages.pytest
  ];

  shellHook = ''
    echo "Morgen Tasks dev environment loaded"
    echo "Python: $(python3 --version)"
  '';
}
