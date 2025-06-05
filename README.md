# スロットホールのイベント日推定と台予測

このリポジトリには Jupyter Notebook `slot_halls_dynamic_base_date_machinepred.ipynb` が含まれています。ノートブックは **min-repo.com** をスクレイピングし、イベント候補日を作成してスロット台の予測を行うためのものです。

## ノートブックの概要
1. `requests` で min-repo.com からホール情報を取得します。
2. 基準日から優先度付きのイベント候補日リストを生成します。
3. 過去データを集計し、ホールごとの実績をまとめます。
4. 簡易的なスコアリングモデルを用いて有望な台を予測します。

## 必要なパッケージ
Python 3 と以下のパッケージが必要です。
- `requests`
- `beautifulsoup4`
- `pandas`
- `numpy`
- `python-dateutil`
- `requests-cache`
- `jupyter`（ノートブック実行用）

次のコマンドでインストールできます。
```bash
pip install requests beautifulsoup4 pandas numpy python-dateutil requests-cache jupyter
```

## ノートブックの起動
以下のいずれかでノートブックを開きます。
```bash
jupyter notebook slot_halls_dynamic_base_date_machinepred.ipynb
```
または
```bash
jupyter lab slot_halls_dynamic_base_date_machinepred.ipynb
```

## requests_cache によるキャッシュ
HTTP リクエストの再ダウンロードを防ぐため、`requests_cache` の利用を推奨します。ノートブックでは次のように設定します。
```python
import requests_cache
requests_cache.install_cache('minrepo_cache', expire_after=60*60*24, backend='sqlite')
```
これにより現在のディレクトリに `minrepo_cache.sqlite` が作成され、24 時間データをキャッシュします。`requests_cache` がインストールされていない場合でも、通常の HTTP リクエストとして動作します。
