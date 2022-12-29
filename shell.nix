with import <nixpkgs> {} ;

let
  my-django-ninja = callPackage /home/lemon/src/my-nix-pkgs/python/django-ninja/default.nix {
      buildPythonPackage = python3Packages.buildPythonPackage;
  };
  python-with-my-packages = python3.withPackages (p: with p; [
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
