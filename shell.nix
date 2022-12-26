{ pkgs ? import <nixpkgs> {} }:

let
  my-python = pkgs.python3;
  python-with-my-packages = my-python.withPackages (p: with p; [
    django
    celery[redis]
    django-crispy-forms
    django-extensions
    factory_boy
    openpyxl
    djangorestframework
    django-ninja
  ]);
in
  pkgs.mkShell {
    DBASIK_SECRET_KEY = "lobbo";
    packages = [
      python-with-my-packages
  ];
}
