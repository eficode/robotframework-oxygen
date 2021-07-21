{ pkgs ? import <nixpkgs> {}
, python ? "python37"
, rfVersion ? "3.0.4"
, cmd ? "green" }:
with pkgs;
let
  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix/";
    ref = "refs/tags/3.3.0";
  }) {
    inherit python;
    pypiDataRev = "c8393888d97e74f2217aaafae70bf5bc5c913535";
    pypiDataSha256 = "0pfivp1w3pdbsamnmmyy4rsnc4klqnmisjzcq0smc4pp908b6sc3";
  };

  package = mach-nix.buildPythonPackage {
    src = ./.;
    requirements = ''
      robotframework==${rfVersion}
      junitparser>=1.2.2
      PyYAML>=3.13

      ### Dev
      mock>=2.0.0
      coverage>=5.1
      testfixtures>=6.14.1 # needed for large dict comparisons to make sense of them
      green>=3.1.3 # unit test runner
    '';
  };
in
  runCommand "${package.pname}-${package.version}-result" {
    buildInputs = [ coreutils package ];
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
