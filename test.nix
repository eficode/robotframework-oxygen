{ nixpkgsBranch ? "release-21.05"
, nixpkgs ? "https://github.com/NixOS/nixpkgs/archive/refs/heads/${nixpkgsBranch}.tar.gz"
, pythons ? "python37 python38 python39"
, rfVersions ? "3.0.4 3.2.2 4.0.3 4.1"
, path ? toString ./.
, cmd ? "invoke test --in-nix" }:
let
  pkgs = import (fetchTarball nixpkgs) { };
in
with pkgs;
with lib;
let
  test = python: rfVersion:
    import ./default.nix { inherit nixpkgs python rfVersion path cmd; };

  pythons' = splitString " " pythons;
  rfVersions' = splitString " " rfVersions;

  tests = flatten (map (rfVersion: map (python: test python rfVersion) pythons') rfVersions');
in
  runCommand "test-results" {
    buildInputs = [ coreutils ];
  } (''
    mkdir -p $out
    echo "python,rfVersion,state,log" >>$out/results.csv
    globalState="ok"
  '' + (concatMapStringsSep "\n" (test: ''
    python="$(cat ${test}/python)"
    rfVersion="$(cat ${test}/rfVersion)"
    if [ "0" = "$(cat ${test}/exitCode)" ]
    then
      state="ok"
    else
      state="error"
      globalState="error"
    fi
    testpath="$out/$python/$rfVersion"
    mkdir -p "$testpath"
    cp "${test}/exitCode" "$testpath/"
    cp "${test}/log" "$testpath/"
    echo "$python,$rfVersion,$state,$testpath/log" >>$out/results.csv
  '') tests) + ''

    echo "$globalState" >$out/state
  '')
