{ nixpkgs ? https://github.com/NixOS/nixpkgs/archive/refs/heads/nixos-unstable.tar.gz
, python ? "python37"
, rfVersion ? "3.0.4"
, path ? toString ./.
, cmd ? "green" }:
let
  pkgs = import (fetchTarball nixpkgs) { };
in
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

  requirementsWithout = names:
    let
      requirementsFile = names: runCommand "requirements.txt" {
        buildInputs = [ gnused ];
      } ''
        cp "${/. + "${path}/requirements.txt"}" $out
        for name in ${toString names}
        do
          sed -E "/^$name([=<>]|\$)/d" -i $out
        done
      '';
    in
      readFile (requirementsFile names);

  package = mach-nix.buildPythonPackage {
    pname = "robotframework-oxygen";
    version = "dev";
    src = /. + path;
    requirements = requirementsWithout ["robotframework" "twine"];
    requirementsExtra = ''
      robotframework==${rfVersion}
    '';
  };
in
  runCommand "${package.pname}-${package.version}-result" {
    buildInputs = [ coreutils package ];
    shellHook = ''
      tmpdir="$(mktemp -d -t src-XXXXXXXXXX)"
      trap "rm -rf $tmpdir" EXIT
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
    tmpdir="$(mktemp -d -t src-XXXXXXXXXX)"
    trap "rm -rf $tmpdir" EXIT
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
