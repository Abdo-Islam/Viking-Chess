{ pkgs ? import <nixpkgs> {} }:
let
  python = pkgs.python3;
  pythonPackages = python.pkgs;
  lib = pkgs.lib;

  # Define salat dependency manually from PyPI
  pysimplegui = pythonPackages.buildPythonPackage rec {
    pname = "pysimplegui";
    version = "6.0";
    src = pythonPackages.fetchPypi {
      inherit pname version;
      sha256 = "sha256-UI+nFaT+zc3l10sgv0cxUbxdV1iLmFHMnXgVGcP72H0=";
      # Replace this with the actual hash from nix build error (see below)
    };

    format = "setuptools";
    doCheck = false;
  };

in
  pythonPackages.buildPythonPackage rec {
    pname = "viking";
    version = "0.2.0";
    src = ./.;
    format = "setuptools";

    propagatedBuildInputs = with pythonPackages; [
      setuptools
      pysimplegui
    ];

    doCheck = false;

    meta = with pkgs.lib; {
      description = "A python program to print the next salah and remaining time.";
      homepage = "https://github.com/pxlman/next-salah";
      license = licenses.mit;
    };
  }

