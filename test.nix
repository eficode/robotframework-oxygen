/* Nix script for running tests with different combinations of Python and
  Robot Framework versions in one go.

  Currently this script is not being used by CI/CD but is an option to run
  matrix style tests on user's machine.

  Example:
  $ nix-build test.nix --argstr pythons "python38 python39" \
      --argstr rfVersions "3.1.2 3.2 3.2.1 3.2.2"

  Example command will run following tests in parallel:
  - latest Python 3.8 with Robot Framework 3.1.2
  - latest Python 3.9 with Robot Framework 3.1.2
  - latest Python 3.8 with Robot Framework 3.2
  - latest Python 3.9 with Robot Framework 3.2
  - latest Python 3.8 with Robot Framework 3.2.1
  - latest Python 3.9 with Robot Framework 3.2.1
  - latest Python 3.8 with Robot Framework 3.2.2
  - latest Python 3.9 with Robot Framework 3.2.2

  Results:
  Command will always exit with exit code 0 (unless there is an issue with
  the script itself or passing unsupported versions of Python, Robot Framework
  or dependencies inside `requirements.txt`).

  The results are in `./result` directory.

    - `./result/state` file will contain value of `ok` or `fail` and is representing the overall state of tests
    - `./result/<python>/<rfVersion>/` directory contains files `exitCode` and `log` for each test run
*/
{ nixpkgsBranch ? "release-21.05"
, nixpkgs ? "https://github.com/NixOS/nixpkgs/archive/refs/heads/${nixpkgsBranch}.tar.gz"
, pythons ? "python38 python39"
, rfVersions ? "3.1.2 3.2 3.2.1 3.2.2 4.0 4.0.1 4.0.2 4.0.3 4.1"
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
    buildInputs = [ coreutils gnused ];
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
      state="fail"
      globalState="fail"
    fi
    testpath="$out/$python/$rfVersion"
    mkdir -p "$testpath"
    cp "${test}/exitCode" "$testpath/"
    cp "${test}/log" "$testpath/"
    echo "$python,$rfVersion,$state,$testpath/log" >>$out/results.csv
  '') tests) + ''

    echo "$globalState" >$out/state

    sed "s/,/\t/g" <(tail -n +2 "$out/results.csv")
    echo -e "\nOverall tests state: $globalState"
  '')
