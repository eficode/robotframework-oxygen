{ nixpkgsBranch ? "release-21.05"
, nixpkgs ? "https://github.com/NixOS/nixpkgs/archive/refs/heads/${nixpkgsBranch}.tar.gz"
, python ? "python37"
, rfVersion ? "3.0.4"
, path ? toString ./.
, cmd ? "invoke test --in-nix" }:
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
    inherit pkgs python;
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

  pname = "robotframework-oxygen";
  requirements = ''
    ${requirementsWithout ["robotframework" "twine"]}
    robotframework==${rfVersion}
  '';

  env = mach-nix.mkPython {
    inherit requirements;
  };
in
  runCommand "${pname}-result" {
    buildInputs = [ which coreutils env ];
    shellHook = ''
      cd ${path}
      export PYTHONPATH="$PWD/src:${env}/lib/${env.python.libPrefix}/site-packages"
      ${cmd}
      exitCode=$?
      echo -e "\n[${python}][robotframework==${rfVersion}] Exited with $exitCode"
      exit $exitCode
    '';
  } ''
    mkdir -p $out
    tmpdir="$(mktemp -d -t ${pname}-XXXXXXXXXX)"
    trap "rm -rf $tmpdir" EXIT
    cp -r ${/. + path} $tmpdir/src
    chmod -R u+w $tmpdir
    cd $tmpdir/src
    export PYTHONPATH="$PWD/src:${env}/lib/${env.python.libPrefix}/site-packages"
    export HOME=$tmpdir
    echo '{"run":{"shell":"${stdenv.shell}"}}' >$HOME/.invoke.json
    exec &> >(tee $out/log)
    set +e
    ${cmd}
    exitCode=$?
    set -e
    echo -e "\n[${python}][robotframework==${rfVersion}] Exited with $exitCode"
    echo "$exitCode" > $out/exitCode
    echo "${python}" > $out/python
    echo "${rfVersion}" > $out/rfVersion
  ''
