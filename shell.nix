let 
pkgs = import <nixpkgs> {};
viking = pkgs.callPackage ./default.nix {};
in
pkgs.mkShell {
  buildInputs = [
    viking
    ];
}

