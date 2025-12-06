#!/usr/bin/env python3
"""
ITEE過去問サイトのHTML生成スクリプト
problems.jsonからモダンなHTMLを自動生成
"""

import json
from datetime import datetime

def load_problems():
    """problems.jsonを読み込む"""
    with open('problems.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_html(problems):
    """モダンなHTMLを生成"""
    
    # タグ一覧を抽出
    all_tags = set()
    for p in problems:
        all_tags.update(p['tags'])
    sorted_tags = sorted(all_tags)
    
    # 年度一覧を抽出
    years = sorted(set(p['year'] for p in problems), reverse=True)
    
    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>情報処理技術者試験の過去問を実際に動かしてみよう!</title>
    <meta name="description" content="情報処理技術者試験(基本情報・応用情報)の過去問をPythonで実装して動かしてみよう。アルゴリズム問題を実際に動かすことで理解を深めます。">
    
    <!-- Open Graph / Twitter Card -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="情報処理技術者試験の過去問を実際に動かしてみよう!">
    <meta property="og:description" content="過去問をPythonで実装して理解を深める">
    <meta property="og:url" content="https://maehrm.github.io/itee/">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --bg-card: #ffffff;
            --text-primary: #212529;
            --text-secondary: #6c757d;
            --accent-color: #0066cc;
            --border-color: #dee2e6;
            --shadow: 0 2px 8px rgba(0,0,0,0.1);
            --shadow-hover: 0 4px 16px rgba(0,0,0,0.15);
        }}
        
        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg-primary: #1a1a1a;
                --bg-secondary: #2d2d2d;
                --bg-card: #2d2d2d;
                --text-primary: #e9ecef;
                --text-secondary: #adb5bd;
                --accent-color: #4d9fff;
                --border-color: #495057;
                --shadow: 0 2px 8px rgba(0,0,0,0.3);
                --shadow-hover: 0 4px 16px rgba(0,0,0,0.4);
            }}
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", "Hiragino Sans", "Hiragino Kaku Gothic ProN", Meiryo, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            transition: background 0.3s, color 0.3s;
        }}
        
        header {{
            background: var(--bg-secondary);
            padding: 2rem 1rem;
            text-align: center;
            border-bottom: 1px solid var(--border-color);
        }}
        
        h1 {{
            font-size: 1.75rem;
            margin-bottom: 1rem;
            color: var(--accent-color);
        }}
        
        .subtitle {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .social-buttons {{
            margin-top: 1rem;
            display: flex;
            gap: 0.5rem;
            justify-content: center;
            align-items: center;
        }}
        
        .stats {{
            background: var(--bg-secondary);
            padding: 1rem;
            text-align: center;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .stats-container {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            gap: 2rem;
            justify-content: center;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: var(--accent-color);
        }}
        
        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        
        .controls {{
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }}
        
        .filter-section {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }}
        
        .filter-title {{
            font-weight: bold;
            margin-bottom: 0.75rem;
            color: var(--text-primary);
        }}
        
        .filter-buttons {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        
        .filter-btn {{
            padding: 0.4rem 0.8rem;
            border: 1px solid var(--border-color);
            background: var(--bg-card);
            color: var(--text-primary);
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.2s;
        }}
        
        .filter-btn:hover {{
            background: var(--accent-color);
            color: white;
            border-color: var(--accent-color);
        }}
        
        .filter-btn.active {{
            background: var(--accent-color);
            color: white;
            border-color: var(--accent-color);
        }}
        
        .search-box {{
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 1rem;
            background: var(--bg-card);
            color: var(--text-primary);
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}
        
        .problems-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.5rem;
        }}
        
        .problem-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            transition: all 0.3s;
            box-shadow: var(--shadow);
        }}
        
        .problem-card:hover {{
            box-shadow: var(--shadow-hover);
            transform: translateY(-4px);
        }}
        
        .problem-meta {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 0.75rem;
            flex-wrap: wrap;
        }}
        
        .badge {{
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
        }}
        
        .badge-year {{
            background: #e3f2fd;
            color: #1976d2;
        }}
        
        .badge-exam {{
            background: #f3e5f5;
            color: #7b1fa2;
        }}
        
        @media (prefers-color-scheme: dark) {{
            .badge-year {{
                background: #1565c0;
                color: #bbdefb;
            }}
            .badge-exam {{
                background: #6a1b9a;
                color: #e1bee7;
            }}
        }}
        
        .problem-title {{
            font-size: 1rem;
            margin-bottom: 0.75rem;
            color: var(--text-primary);
            line-height: 1.4;
        }}
        
        .problem-link {{
            color: var(--accent-color);
            text-decoration: none;
            font-weight: 500;
        }}
        
        .problem-link:hover {{
            text-decoration: underline;
        }}
        
        .tag-container {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-top: 0.75rem;
        }}
        
        .tag {{
            background: var(--bg-secondary);
            color: var(--text-secondary);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
        }}
        
        .no-results {{
            text-align: center;
            padding: 3rem 1rem;
            color: var(--text-secondary);
        }}
        
        footer {{
            background: var(--bg-secondary);
            padding: 2rem 1rem;
            text-align: center;
            margin-top: 4rem;
            border-top: 1px solid var(--border-color);
        }}
        
        footer a {{
            color: var(--accent-color);
            text-decoration: none;
        }}
        
        footer a:hover {{
            text-decoration: underline;
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 1.5rem;
            }}
            
            .problems-grid {{
                grid-template-columns: 1fr;
            }}
            
            .stats-container {{
                gap: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>📚 情報処理技術者試験の過去問を実際に動かしてみよう!</h1>
        <p class="subtitle">
            情報処理技術者試験(基本情報・応用情報)に合格するために、問題を紙上で解くだけでなく、<br>
            実際に動かしてみるという勉強法もよいのではと思います。参考になれば…。
        </p>
        <div class="social-buttons">
            <a href="http://b.hatena.ne.jp/entry/s/maehrm.github.io/itee/" target="_blank">
                <img src="https://b.st-hatena.com/images/v4/public/entry-button/button-only@2x.png" 
                     alt="このエントリーをはてなブックマークに追加" 
                     style="height: 20px; border: none;">
            </a>
            <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" 
               class="twitter-share-button" 
               data-show-count="false">Tweet</a>
        </div>
    </header>
    
    <div class="stats">
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number" id="total-count">{len(problems)}</div>
                <div class="stat-label">問題数</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{len(years)}</div>
                <div class="stat-label">年度</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{len(sorted_tags)}</div>
                <div class="stat-label">タグ種類</div>
            </div>
        </div>
    </div>
    
    <div class="controls">
        <div class="filter-section">
            <div class="filter-title">🔍 検索</div>
            <input type="text" 
                   id="search-input" 
                   class="search-box" 
                   placeholder="問題を検索... (タイトル、年度、タグなど)">
        </div>
        
        <div class="filter-section">
            <div class="filter-title">📅 年度</div>
            <div class="filter-buttons">
                <button class="filter-btn active" data-filter="year" data-value="all">すべて</button>
'''
    
    # 年度フィルターボタンを追加
    for year in years:
        html += f'                <button class="filter-btn" data-filter="year" data-value="{year}">{year}</button>\n'
    
    html += '''            </div>
        </div>
        
        <div class="filter-section">
            <div class="filter-title">📖 試験種別</div>
            <div class="filter-buttons">
                <button class="filter-btn active" data-filter="exam" data-value="all">すべて</button>
                <button class="filter-btn" data-filter="exam" data-value="応用情報">応用情報</button>
                <button class="filter-btn" data-filter="exam" data-value="基本情報">基本情報</button>
                <button class="filter-btn" data-filter="exam" data-value="ソフトウェア開発">ソフトウェア開発</button>
            </div>
        </div>
        
        <div class="filter-section">
            <div class="filter-title">🏷️ タグ</div>
            <div class="filter-buttons">
                <button class="filter-btn active" data-filter="tag" data-value="all">すべて</button>
'''
    
    # タグフィルターボタンを追加
    for tag in sorted_tags:
        html += f'                <button class="filter-btn" data-filter="tag" data-value="{tag}">{tag}</button>\n'
    
    html += '''            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="problems-grid" id="problems-grid">
'''
    
    # 各問題カードを生成
    for p in problems:
        tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in p['tags']])
        
        html += f'''            <div class="problem-card" 
                 data-year="{p['year']}" 
                 data-exam="{p['exam']}" 
                 data-tags="{','.join(p['tags'])}"
                 data-search="{p['year']} {p['exam']} {p['title']} {' '.join(p['tags'])}">
                <div class="problem-meta">
                    <span class="badge badge-year">{p['year']}</span>
                    <span class="badge badge-exam">{p['exam']} {p['question']}</span>
                </div>
                <div class="problem-title">
                    <a href="{p['url']}" target="_blank" class="problem-link">
                        {p['title']}
                    </a>
                </div>
                <div class="tag-container">
                    {tags_html}
                </div>
            </div>
'''
    
    html += '''        </div>
        <div class="no-results" id="no-results" style="display: none;">
            該当する問題が見つかりませんでした。
        </div>
    </div>
    
    <footer>
        <p>
            Last updated: ''' + datetime.now().strftime('%Y-%m-%d') + '''<br>
            Ⓜⓐⓢⓐⓗⓘⓓⓔ Ⓜⓐⓔⓗⓐⓡⓐ (<a href="https://twitter.com/maehrm" target="_blank">@maehrm</a>)
        </p>
    </footer>
    
    <script>
        const problems = ''' + json.dumps(problems, ensure_ascii=False) + ''';
        
        let currentFilters = {
            year: 'all',
            exam: 'all',
            tag: 'all',
            search: ''
        };
        
        // フィルターボタンのクリックイベント
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const filterType = this.dataset.filter;
                const value = this.dataset.value;
                
                // 同じグループのボタンのactiveを外す
                document.querySelectorAll(`[data-filter="${filterType}"]`).forEach(b => {
                    b.classList.remove('active');
                });
                
                // クリックされたボタンをactiveに
                this.classList.add('active');
                
                // フィルター設定を更新
                currentFilters[filterType] = value;
                
                // フィルター適用
                applyFilters();
            });
        });
        
        // 検索ボックス
        document.getElementById('search-input').addEventListener('input', function(e) {
            currentFilters.search = e.target.value.toLowerCase();
            applyFilters();
        });
        
        // フィルター適用関数
        function applyFilters() {
            const cards = document.querySelectorAll('.problem-card');
            let visibleCount = 0;
            
            cards.forEach(card => {
                let show = true;
                
                // 年度フィルター
                if (currentFilters.year !== 'all' && card.dataset.year !== currentFilters.year) {
                    show = false;
                }
                
                // 試験種別フィルター
                if (currentFilters.exam !== 'all' && card.dataset.exam !== currentFilters.exam) {
                    show = false;
                }
                
                // タグフィルター
                if (currentFilters.tag !== 'all') {
                    const tags = card.dataset.tags.split(',');
                    if (!tags.includes(currentFilters.tag)) {
                        show = false;
                    }
                }
                
                // 検索フィルター
                if (currentFilters.search && !card.dataset.search.toLowerCase().includes(currentFilters.search)) {
                    show = false;
                }
                
                card.style.display = show ? 'block' : 'none';
                if (show) visibleCount++;
            });
            
            // 結果なしメッセージの表示/非表示
            document.getElementById('no-results').style.display = visibleCount === 0 ? 'block' : 'none';
            
            // 表示件数を更新
            document.getElementById('total-count').textContent = visibleCount;
        }
        
        // Twitter ボタンスクリプト
        !function(d,s,id){
            var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';
            if(!d.getElementById(id)){
                js=d.createElement(s);
                js.id=id;
                js.src=p+'://platform.twitter.com/widgets.js';
                fjs.parentNode.insertBefore(js,fjs);
            }
        }(document, 'script', 'twitter-wjs');
    </script>
</body>
</html>
'''
    
    return html

def main():
    """メイン処理"""
    print("ITEE過去問サイト生成中...")
    
    # データ読み込み
    problems = load_problems()
    print(f"✅ {len(problems)}問のデータを読み込みました")
    
    # HTML生成
    html = generate_html(problems)
    print("✅ HTMLを生成しました")
    
    # ファイル出力
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅ index.htmlを出力しました")
    
    print("\n🎉 完了!")
    print("📁 生成されたファイル:")
    print("   - index.html")

if __name__ == '__main__':
    main()
