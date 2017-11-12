{ pkgs ? import <nixpkgs> {}}:

with pkgs;

let
  python = python3;
  pythonPackages = python.pkgs;

  # generated with `pip2nix generate -r requirements.txt`
  generatePipPackages = import ./python-packages.nix {
    inherit pkgs;
    inherit (pkgs) fetchurl fetchgit fetchhg;
  };

  pipPackages =  generatePipPackages pipPackages pythonPackages;
in

pythonPackages.buildPythonApplication rec {
  pname = "lingualeo2anki";
  version = "0.0.1";
  name = "${pname}-${version}";
  namePrefix = "";

  src = ./.;

  buildInputs = with pythonPackages; [
    python
    pbr
    git
    glibcLocales
  ];

  propagatedBuildInputs = with pipPackages; [
    colorama
    requests
    beautifulsoup4
    memoized-property
  ];

  # will fail with `UnicodeEncodeError: 'ascii' codec can't encode` without this
  preConfigure = ''
    export LC_ALL="en_US.UTF-8"
  '';

  meta = {
    homepage = https://github.com/BjornMelgaard/lingualeo2anki;
    description = "Hack lingualeo chrome plugin and save dictionary locally, ready for anki import";
    license = lib.licenses.mit;
    platforms = lib.platforms.all;
  };
}

