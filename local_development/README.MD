I think development should be IDE agnostic. This directory will be used to store my vscode/docker settings. Below is a shell script I use to clone this repo and set up vscode. If you prefer a different development environment, ignore this.


```bash
buhruce@macbook Desktop % which ninja
/usr/local/bin/ninja
buhruce@macbook Desktop % cat /usr/local/bin/ninja
rm -Rf ~/Desktop/ninja/
cd ~/Desktop
git clone git@github.com:buhruce/ninja.git
cp -R ~/Desktop/ninja/local_development/.devcontainer ~/Desktop/ninja/.devcontainer
cp ~/.localdev/ninjaDockerfile ~/Desktop/ninja/Dockerfile
code ~/Desktop/ninja
```
