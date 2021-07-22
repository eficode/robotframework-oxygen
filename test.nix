{ nixpkgs ? https://github.com/NixOS/nixpkgs/archive/refs/heads/nixos-unstable.tar.gz
, cmd ? "green" }:
let
  pkgs = import (fetchTarball nixpkgs) { };
in
with pkgs;
with lib;
let
  test = python: rfVersion:
    import ./default.nix { inherit nixpkgs python rfVersion cmd; };

  pythons = [ "python36" "python37" "python38" "python39" /* "python310" */ ];
  rfVersions = [ "3.0.4" "3.1.2" "3.2.2" "4.0.3" "4.1" ];
in
  buildEnv {
    name = "results";
    paths = flatten (map (rfVersion: map (python: test python rfVersion) pythons) rfVersions);
    pathsToLink = [ "/" ];
  }
