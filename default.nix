{ pkgs ? import <nixpkgs> {}}:

with pkgs;

let
  python = python3;
  pythonPackages = python.pkgs;

  # generated with `pip2nix generate -r requirements.txt`
  pythonPackagesGenerated = import ./python-packages.nix {
    inherit pkgs;
    inherit (pkgs) fetchurl fetchgit fetchhg;
  };

  allPythonPackages =  pythonPackagesGenerated allPythonPackages pythonPackages;
in

pythonPackages.buildPythonPackage rec {
  pname = "lingualeo2anki";
  version = "0.0.1";
  name = "${pname}-${version}";

  src = ./.;

  buildInputs = with allPythonPackages; [
    python

    colorama
    requests
    beautifulsoup4
    memoized-property
  ];
}
