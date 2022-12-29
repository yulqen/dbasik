with import <nixpkgs> {} ;

let
  my-django-ninja = callPackage /home/lemon/src/nix-pkgs/django-ninja/default.nix {
      buildPythonPackage = python3Packages.buildPythonPackage;
  };
  my-python = python3;
  python-with-my-packages = my-python.withPackages (p: with p; [
    django
    celery[redis]
    django-crispy-forms
    django-extensions
    factory_boy
    openpyxl
    djangorestframework
    my-django-ninja
  ]);
in
  pkgs.mkShell {
    DBASIK_SECRET_KEY = "lobbo";
    packages = [
      python-with-my-packages
  ];
}
