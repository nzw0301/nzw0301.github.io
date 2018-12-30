---
layout: post
title: "OSXにJuliaをインストール"
comments: false
abstract: OSXにjuliaをいれる
---

### はじめに

1年に2回くらいJuliaを書く気持ちになるのだが，v0.3の頃に [SimRank](http://www.slideshare.net/kentonozawa75/cooking-with-julia) をかいてからまともにかいてなかったので，環境を作るところから．
環境は`Sierra`と`EL Capitan`で試した．

### 本題

以前はHomebrewで入れていたのだが， `Pkg.update()` するとエラーが出て使えないので[公式ページ](http://julialang.org/downloads/)からダウンロードする．


この場合，Juliaは`/Applications/Julia-0.5.app/Contents/Resources/julia/bin/julia`にあるのでパスを通す必要がある．
zshやbashであれば`.*shrc`ファイルにかけばいいのだが，
`fish`を使っているので`~/.config/fish/functions/julia.fish`というファイルを作成する．

``` shell
function julia
    /Applications/Julia-0.5.app/Contents/Resources/julia/bin/julia $argv;
end
```

---

`Jupyter` を好んで使うので `IJulia` を入れようとしたが．ビルドでエラーになる．

``` julia
julia> Pkg.build("IJulia")
INFO: Building Conda
INFO: Building Homebrew
Already up-to-date.
INFO: Building Nettle
INFO: Building ZMQ
INFO: Building IJulia
INFO: Installing Jupyter via the Conda package.
INFO: Downloading miniconda installer ...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100   378  100   378    0     0    197      0  0:00:01  0:00:01 --:--:--     0
INFO: Installing miniconda ...
/Users/nzq/.julia/v0.5/Conda/deps/usr/installer.sh: line 1: syntax error near unexpected token `newline'
/Users/nzw/.julia/v0.5/Conda/deps/usr/installer.sh: line 1: `<html>'

julia>
```

`conda.jl` で失敗してるので[conda.jlのページ](https://github.com/JuliaPy/Conda.jl#using-an-already-existing-conda-installation)をみるとそれっぽいのがあるのでそれに従う．

``` shell
$ conda create -n conda_jl python
$ export CONDA_JL_HOME="/Users/nzq/.pyenv/versions/miniconda3-latest/"envs/conda_jl/
> julia
julia> Pkg.build("Conda")
julia> Pkg.build("IJulia")
```


---

エディタは，[atom+Juno](https://github.com/JunoLab/uber-juno/blob/master/setup.md#getting-atom--juno)がmatlabみたいに使えるのでかなりよい．
