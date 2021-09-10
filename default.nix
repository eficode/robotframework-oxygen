/* Nix script used primarily for running tests per one specific Python version
  and one specific Robot Framework version.

  For running this script Nix has to be installed on system, the rest of the
  dependencies (Python and other dependencies) will be taken care of by Nix itself.

  Python packages are supplied by Nix while Robot Framework is fetched from PyPi

  Running tests:
    All arguments are optional, by default latest Python 3.9,
    Robot Framework 3.2.2 is used and tests are being run with command `invoke test --in-nix`

    Example:
    $ nix-build --argstr python python39 --argstr rfVersion 3.2.2 --argstr cmd "invoke test --in-nix"

  Secondary function of this script is development environment:
    User can use nix-shell to drop into development shell with all dependencies needed for the project,
    without the need to separately install all supported Python versions and/or other dependencies on your own.

    Example:
    This will drop the user into subshell with latest Python 3.8 and Robot Framework version 3.0.4,
    ready to run tests or your favorite editor out of it (so it is running in correct environment)
    $ nix-shell --argstr python python38 --argstr rfVersion 3.0.4 --argstr cmd "$SHELL"
*/
{ nixpkgsBranch ? "release-21.05"
, nixpkgs ? "https://github.com/NixOS/nixpkgs/archive/refs/heads/${nixpkgsBranch}.tar.gz"
, python ? "python39"
, rfVersion ? "3.2.2"
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
    pypiDataRev = "5c6e5ecbc5a60fb9c43dc77be8e0eb8ac89f4fee";
    pypiDataSha256 = "0gnq6r92bmnhqjykx3jff7lvg7wbpayd0wvb0drra8r8dvmr5b2d";
  };

  /* Returns new line delimited dependencies in format of `requirements.txt`
    without the specific dependencies that are passed as list of strings.

    The `requirements.txt` is picked up from root directory of the project.

    Example of requirements.txt content:
    ```
    foo==1.2.3
    bar<2.0
    baz==2.3.4
    qux
    ```

    Example run:
    result = requirementsWithout ['foo', 'qux']

    Result for this example:
    ```
    bar<2.0
    baz==2.3.4
    ```
  */
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
    ${requirementsWithout ["robotframework"]}
    robotframework==${rfVersion}
    setuptools
  '';

  env = mach-nix.mkPython {
    inherit requirements;
  };
in
  runCommand "${pname}-result" {
    buildInputs = [ which coreutils env ];
    # Hook for when the file is being run with nix-shell for the devel environment
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
