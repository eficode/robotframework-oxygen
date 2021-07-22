{ pkgs ? import <nixpkgs> {}
, python ? "python37"
, rfVersion ? "3.0.4"
, cmd ? "green" }:
with pkgs;
with lib;
let
  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix/";
    ref = "refs/tags/3.3.0";
  }) {
    inherit python;
    pypiDataRev = "c8393888d97e74f2217aaafae70bf5bc5c913535";
    pypiDataSha256 = "0pfivp1w3pdbsamnmmyy4rsnc4klqnmisjzcq0smc4pp908b6sc3";
  };

  requirements =
    let
      lines = splitString "\n" (readFile ./requirements.txt);
      removeComments = filter (line: line != "" && !(hasPrefix "#" line));
      removeEntry = prefix: lines: filter (line: !(hasPrefix prefix line)) lines;
    in
      concatStringsSep "\n" (removeEntry "robotframework" (removeComments lines));

  package = mach-nix.buildPythonPackage {
    pname = "robotframework-oxygen";
    version = "dev";
    src = ./.;
    inherit requirements;
    requirementsExtra = ''
      robotframework==${rfVersion}
    '';
  };
in
  runCommand "${package.pname}-${package.version}-result" {
    buildInputs = [ coreutils package ];
    shellHook = ''
      tmpdir=$(mktemp -d -t src-XXXXXXXXXX)
      cp -r ${package.src}/* $tmpdir/
      chmod -R u+w $tmpdir
      cd $tmpdir
      ${cmd}
      exit_code=$?
      echo -e "\n[${python}][robotframework==${rfVersion}] Exited with $exit_code"
      exit $exit_code
    '';
  } ''
    outpath="$out/${python}/robotframework-${rfVersion}";
    mkdir -p $outpath
    tmpdir=$(mktemp -d -t src-XXXXXXXXXX)
    cp -r ${package.src}/* $tmpdir/
    chmod -R u+w $tmpdir
    cd $tmpdir
    exec &> >(tee $outpath/log)
    set +e
    ${cmd}
    exit_code=$?
    set -e
    echo -e "\n[${python}][robotframework==${rfVersion}] Exited with $exit_code"
    echo "{\"python\":\"${python}\",\"robotframework\":\"${rfVersion}\",\"exit\":\"$exit_code\"}" > $outpath/result
  ''
