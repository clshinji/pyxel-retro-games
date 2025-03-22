# レトロゲーム集

これは pyxel で作成したゲームを個人的にまとめておくためのリポジトリです。
作成したゲームは games ディレクトリにまとめてあります。（随時更新予定）

pyxel については、[pyxel の公式サイト](https://github.com/kitao/pyxel/blob/main/docs/README.ja.md) を参照してください。

また、pyxel のわかりやすい動画は [Pyxel で簡単にレトロゲームを作成！初心者でも Python でゲームが作れる！(Python プログラミング VTuber サプー)](https://www.youtube.com/watch?v=0g0L5iGKv9g) が分かりやすいのでおすすめです。

# デプロイメモ

## 仮想環境を有効化する

pyxel ディレクトリで実行する

```
source env_pyxel/bin/activate
```

## Python でゲームを実行する

ゲーム用ディレクトリ (my_game) で実行

```
python game.py
```

## エディタを起動

ゲーム用ディレクトリ (my_game) で実行

```
pyxel edit my_resource.pyxres
```

## HTML ファイルの作成

pyxel ディレクトリで実行する。

```
pyxel package my_game my_game/game.py
cd web
pyxel app2html ../my_game.pyxapp
mv my_game.html index.html
cd ..
```

## デプロイ手順

### S3 にアップロード

pyxel ディレクトリで実行する。

```
aws s3 cp web/index.html s3://pyxel-apps-clshinji/index.html
```

### CloudFront の操作

index.html を強制的に公開する（キャッシュ削除）

```
aws cloudfront create-invalidation --distribution-id E2NG247DOZH6YH --paths /index.html
```

# 以下、開発用メモ

## やりたいこと

- ホーム画面を Next.js で作る
- ゲームを増やす
- ユーザ管理・スコア管理機能を追加する
  - ユーザごとにスコア、プレイ回数等の情報を記録するようにする
  - ユーザ情報を記録するか？(pyxel で DynamoDB 使える？)

## my_game のアップデート候補

- タイトル画面にハイスコアを表示しておく
- パワーアップアイテムを追加する
  - パワーアップアイテムの候補
    - 一定時間無敵
    - 一定時間プレイヤのスピードを上げる
    - 一定時間石の数を減らす
    - 一定時間石の数を増やす
