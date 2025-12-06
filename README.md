# ITEE過去問サイト モダン化プロジェクト

## 概要
情報処理技術者試験の過去問サイトをモダンなデザインに刷新しました。

## 主な改善点

### 1. デザイン
- **カード型レイアウト**: 各問題がカードとして表示され、見やすく整理
- **ダークモード対応**: システムの設定に自動対応
- **レスポンシブデザイン**: スマホ・タブレット・PCすべてで快適に閲覧可能
- **ホバーエフェクト**: カードにマウスを乗せると浮き上がるアニメーション

### 2. 機能
- **リアルタイム検索**: タイトル、年度、タグで即座に絞り込み
- **多重フィルター**: 年度・試験種別・タグで絞り込み可能
- **統計表示**: 問題数、年度数、タグ種類を表示
- **動的カウント**: フィルター適用時に表示件数がリアルタイム更新

### 3. データ管理
- **JSON分離**: problems.jsonにデータを分離
- **自動生成**: generate.pyでHTMLを自動生成
- **拡張性**: 新しい問題を追加しやすい構造

## ファイル構成

```
itee-modernize/
├── problems.json      # 99問のデータ(JSON形式)
├── generate.py        # HTML生成スクリプト
├── index.html         # 生成されたHTML
└── README.md          # このファイル
```

## 使い方

### 新しい問題を追加する

1. `problems.json`に新しいエントリを追加:
```json
{
  "id": 100,
  "year": "令和8年度春期",
  "exam": "応用情報",
  "question": "午後問3",
  "title": "新しい問題のタイトル",
  "url": "https://maehrm.hatenablog.com/entry/...",
  "tags": ["タグ1", "タグ2"]
}
```

2. HTMLを再生成:
```bash
python3 generate.py
```

### タグ一覧

現在使用されているタグ:
- 探索アルゴリズム (幅優先探索、深さ優先探索、バックトラック)
- グラフ・木構造 (ダイクストラ法、2分探索木、最短経路)
- ソート (ヒープソート、マージソート、クイックソート)
- 動的計画法 (ナップザック問題、編集距離、LCS)
- 文字列 (検索、圧縮、パターンマッチング)
- ビット演算
- 数値計算
- 機械学習
- その他

## 技術仕様

- **HTML5 + CSS3 + Vanilla JavaScript**
- CSSカスタムプロパティでテーマ管理
- `prefers-color-scheme`でダークモード自動検出
- Flexbox/Gridでレスポンシブレイアウト
- JavaScriptでリアルタイムフィルタリング

## デプロイ

GitHub Pagesにデプロイする場合:

1. GitHubリポジトリにpush
2. Settings > Pages > Source を "main" ブランチに設定
3. `https://maehrm.github.io/itee/` でアクセス可能

## メンテナンス

### HTMLを再生成
```bash
python3 generate.py
```

### データの整合性チェック
```python
import json

with open('problems.json', 'r', encoding='utf-8') as f:
    problems = json.load(f)
    
# 重複IDチェック
ids = [p['id'] for p in problems]
if len(ids) != len(set(ids)):
    print("警告: 重複したIDがあります")

# URLチェック
for p in problems:
    if not p['url'].startswith('https://maehrm.hatenablog.com/'):
        print(f"警告: {p['id']}のURLが不正です")
```

## ライセンス

元サイト: https://maehrm.github.io/itee/
作者: 前原正英 (@maehrm)

## 更新履歴

- 2024-12-06: 初版リリース
  - 99問のデータをJSON化
  - モダンなUIに刷新
  - フィルター・検索機能を追加
  - ダークモード対応
