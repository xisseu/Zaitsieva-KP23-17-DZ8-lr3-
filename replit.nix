cat > replit.nix << 'EOF'
{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.flask
    pkgs.python311Packages.pandas
    pkgs.python311Packages.matplotlib
    pkgs.openssl
  ];
}
EOF