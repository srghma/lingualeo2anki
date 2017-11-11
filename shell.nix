{ pkgs ? import <nixpkgs> {} }:

with pkgs;

let
  f = import ./.;
  drv = callPackage f {};
in
  drv
