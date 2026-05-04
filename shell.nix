let 
pkgs = import <nixpkgs> {};
viking = pkgs.callPackage ./default.nix {};
pysimplegui = pkgs.python3Packages.buildPythonPackage rec {
    pname = "pysimplegui";
    version = "6.0";
    src = pkgs.python3Packages.fetchPypi {
        inherit pname version;
        sha256 = "sha256-UI+nFaT+zc3l10sgv0cxUbxdV1iLmFHMnXgVGcP72H0=";
# Replace this with the actual hash from nix build error (see below)
    };

    format = "setuptools";
    doCheck = false;
};
in
pkgs.mkShell {
  buildInputs = [
    viking
    # pysimplegui
    (pkgs.python312.withPackages (ps: with ps; [ pysimplegui tkinter ]))
    # pkgs.python312Packages.tkinter
    ];
}

