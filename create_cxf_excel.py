import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_cxf_excel():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # Remove initial sheet

    # Fonts
    FONT_NAME = "Meiryo UI"
    font_title = Font(name=FONT_NAME, size=15, bold=True, color="1E242B")
    font_subtitle = Font(name=FONT_NAME, size=9.5, italic=True, color="5A626A")
    font_section = Font(name=FONT_NAME, size=11, bold=True, color="1E242B")
    font_header = Font(name=FONT_NAME, size=9.5, bold=True, color="FFFFFF")
    font_data = Font(name=FONT_NAME, size=9, color="222222")
    font_data_bold = Font(name=FONT_NAME, size=9, bold=True, color="222222")
    font_badge_dark = Font(name=FONT_NAME, size=9, bold=True, color="FFFFFF")
    font_badge_light = Font(name=FONT_NAME, size=9, bold=True, color="1E242B")
    font_small = Font(name=FONT_NAME, size=8.5, color="555555")

    # Fills (Refined Monotone Palette)
    fill_dark_header = PatternFill(start_color="282D33", end_color="282D33", fill_type="solid")  # Dark Charcoal
    fill_sub_header = PatternFill(start_color="444B52", end_color="444B52", fill_type="solid")   # Slate Gray
    fill_section = PatternFill(start_color="EAECEE", end_color="EAECEE", fill_type="solid")      # Soft Silver
    fill_zebra_light = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")  # Crisp Off-White
    fill_white = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

    # Badge Fills (Monotone)
    fill_badge_recommended = PatternFill(start_color="D5DBDB", end_color="D5DBDB", fill_type="solid") # Elegant light slate
    fill_badge_warning = PatternFill(start_color="5D6D7E", end_color="5D6D7E", fill_type="solid")     # Medium charcoal
    fill_badge_danger = PatternFill(start_color="2C3E50", end_color="2C3E50", fill_type="solid")      # Deep charcoal navy
    fill_badge_neutral = PatternFill(start_color="EBEDEF", end_color="EBEDEF", fill_type="solid")     # Pale gray

    # Borders
    bd_thin = Side(style='thin', color='D5D8DC')
    bd_medium = Side(style='medium', color='282D33')
    bd_double = Side(style='double', color='282D33')

    border_cell = Border(left=bd_thin, right=bd_thin, top=bd_thin, bottom=bd_thin)
    border_header = Border(left=bd_thin, right=bd_thin, top=bd_medium, bottom=bd_medium)

    # Alignments
    align_left = Alignment(horizontal='left', vertical='center', wrap_text=True)
    align_center = Alignment(horizontal='center', vertical='center', wrap_text=True)
    align_header = Alignment(horizontal='center', vertical='center', wrap_text=True)

    def apply_sheet_defaults(ws):
        ws.views.sheetView[0].showGridLines = True
        # Iterate all cells in the used area to strictly guarantee Meiryo UI
        for row in range(1, ws.max_row + 1):
            for col in range(1, ws.max_column + 1):
                cell = ws.cell(row=row, column=col)
                if cell.font is None or cell.font.name != FONT_NAME:
                    sz = cell.font.size if cell.font else 9
                    b = cell.font.bold if cell.font else False
                    it = cell.font.italic if cell.font else False
                    colr = cell.font.color if cell.font else "222222"
                    cell.font = Font(name=FONT_NAME, size=sz, bold=b, italic=it, color=colr)

    # =========================================================================
    # SHEET 1: エグゼクティブサマリ
    # =========================================================================
    ws1 = wb.create_sheet(title="エグゼクティブサマリ")

    ws1.merge_cells("A1:G1")
    ws1["A1"] = "Apache CXF 4.0 EOL対応方針およびバージョン選定評価書"
    ws1["A1"].font = font_title
    ws1["A1"].alignment = Alignment(horizontal='left', vertical='center')
    ws1.row_dimensions[1].height = 32

    ws1.merge_cells("A2:G2")
    ws1["A2"] = "〜 CXF 4.0のEOLに伴う「3.6回帰方針」の妥当性検証・技術アーキテクチャ分析・推奨ロードマップ 〜"
    ws1["A2"].font = font_subtitle
    ws1["A2"].alignment = Alignment(horizontal='left', vertical='center')
    ws1.row_dimensions[2].height = 20

    ws1["A4"] = "評価基準年月: 2026年10月 | 調査対象: Apache CXF 3.6.x / 4.0.x / 4.1.x / 4.2.x | 作成種別: エンタープライズ技術選定ドキュメント"
    ws1["A4"].font = font_small
    ws1.row_dimensions[4].height = 18

    # Section 1
    ws1.merge_cells("A6:G6")
    ws1["A6"] = "【結論・最高方針判断】 CXF 4.0 EOLに伴う3.6回帰方針の妥当性判定"
    ws1["A6"].font = font_section
    ws1["A6"].fill = fill_section
    ws1["A6"].alignment = Alignment(horizontal='left', vertical='center', indent=1)
    ws1.row_dimensions[6].height = 26

    headers_row1 = [
        ("A8", "B8", "判定観点"),
        ("C8", "C8", "現行ステータス・事実"),
        ("D8", "D8", "方針判定"),
        ("E8", "F8", "判定理由・技術的根拠"),
        ("G8", "G8", "推奨アクション")
    ]
    ws1.row_dimensions[8].height = 26
    for start_cell, end_cell, title in headers_row1:
        if start_cell != end_cell:
            ws1.merge_cells(f"{start_cell}:{end_cell}")
        ws1[start_cell] = title
        ws1[start_cell].font = font_header
        ws1[start_cell].fill = fill_dark_header
        ws1[start_cell].alignment = align_header
        ws1[start_cell].border = border_header
        # ensure border on merged right
        if start_cell != end_cell:
            ws1[end_cell].border = border_header

    summary_data = [
        (
            "CXF 4.0 の継続利用",
            "2026年2月10日 (v4.0.11) にEOL到達済。\nコミュニティからの新規パッチ・脆弱性(CVE)修正は完全停止。",
            "不可\n(重大リスク)",
            "すでにEOLを迎えており、Webサービス通信という外部接点層に未修正脆弱性が放置される致命的セキュリティリスクがある。",
            "速やかな移行計画策定\n（放置厳禁）"
        ),
        (
            "CXF 3.6 への回帰方針\n（ご質問の検討案）",
            "3.6.xは依然として保守中であるが、これは「javax.* (Jakarta EE 8)」に取り残されたレガシー向けの延命ライン。",
            "原則【非妥当】\n（アンチパターン）",
            "① パッケージ名前空間の逆行（jakarta.* → javax.*）によりソースコード・設定の全損改修が発生。\n② Spring Boot 3系やモダンServletコンテナとの非互換・破綻。\n③ 3.6も遠からずEOLを迎える延命枠であり、二重の技術的負債となる。",
            "採用中止\n（特殊なレガシー制約環境を除き却下）"
        ),
        (
            "CXF 4.1 へのバージョンアップ\n（真の推奨方針）",
            "現行のアクティブ保守ライン（Jakarta EE 10 / JDK 17+ 基準）。\n最新CVEパッチおよびSpring 6.2+完全対応。",
            "【強く推奨】\n（ベストプラクティス）",
            "① 4.0と同じ「jakarta.*」空間のため、ソースコードの大半（アノテーション・設定）をそのまま流用可能。\n② JDK 17およびJakarta EE 10に適合し、今後長期的な保守とセキュリティ保証が得られる。\n③ 移行コスト・検証工数が最小。",
            "CXF 4.1.x への\nアップグレード移行を実施"
        )
    ]

    curr_row = 9
    for i, row in enumerate(summary_data):
        ws1.row_dimensions[curr_row].height = 58
        fill_curr = fill_zebra_light if i % 2 == 1 else fill_white

        ws1.merge_cells(f"A{curr_row}:B{curr_row}")
        ws1[f"A{curr_row}"] = row[0]
        ws1[f"A{curr_row}"].font = font_data_bold
        ws1[f"A{curr_row}"].fill = fill_curr
        ws1[f"A{curr_row}"].alignment = align_left
        ws1[f"A{curr_row}"].border = border_cell
        ws1[f"B{curr_row}"].border = border_cell

        ws1[f"C{curr_row}"] = row[1]
        ws1[f"C{curr_row}"].font = font_data
        ws1[f"C{curr_row}"].fill = fill_curr
        ws1[f"C{curr_row}"].alignment = align_left
        ws1[f"C{curr_row}"].border = border_cell

        ws1[f"D{curr_row}"] = row[2]
        ws1[f"D{curr_row}"].alignment = align_center
        ws1[f"D{curr_row}"].border = border_cell
        if "強く推奨" in row[2]:
            ws1[f"D{curr_row}"].font = font_badge_light
            ws1[f"D{curr_row}"].fill = fill_badge_recommended
        elif "非妥当" in row[2]:
            ws1[f"D{curr_row}"].font = font_badge_dark
            ws1[f"D{curr_row}"].fill = fill_badge_warning
        else:
            ws1[f"D{curr_row}"].font = font_badge_dark
            ws1[f"D{curr_row}"].fill = fill_badge_danger

        ws1.merge_cells(f"E{curr_row}:F{curr_row}")
        ws1[f"E{curr_row}"] = row[3]
        ws1[f"E{curr_row}"].font = font_data
        ws1[f"E{curr_row}"].fill = fill_curr
        ws1[f"E{curr_row}"].alignment = align_left
        ws1[f"E{curr_row}"].border = border_cell
        ws1[f"F{curr_row}"].border = border_cell

        ws1[f"G{curr_row}"] = row[4]
        ws1[f"G{curr_row}"].font = font_data_bold
        ws1[f"G{curr_row}"].fill = fill_curr
        ws1[f"G{curr_row}"].alignment = align_center
        ws1[f"G{curr_row}"].border = border_cell

        curr_row += 1

    # Section 2
    curr_row += 2
    ws1.merge_cells(f"A{curr_row}:G{curr_row}")
    ws1[f"A{curr_row}"] = "【クイック診断】貴社システムの状況に応じた最適移行判断フロー"
    ws1[f"A{curr_row}"].font = font_section
    ws1[f"A{curr_row}"].fill = fill_section
    ws1[f"A{curr_row}"].alignment = Alignment(horizontal='left', vertical='center', indent=1)
    ws1.row_dimensions[curr_row].height = 26

    curr_row += 2
    ws1.merge_cells(f"A{curr_row}:B{curr_row}")
    ws1[f"A{curr_row}"] = "現在のシステム要件・環境条件"
    ws1[f"A{curr_row}"].font = font_header
    ws1[f"A{curr_row}"].fill = fill_dark_header
    ws1[f"A{curr_row}"].alignment = align_header
    ws1[f"A{curr_row}"].border = border_header
    ws1[f"B{curr_row}"].border = border_header

    ws1.merge_cells(f"C{curr_row}:E{curr_row}")
    ws1[f"C{curr_row}"] = "技術的制約の判定・メカニズム"
    ws1[f"C{curr_row}"].font = font_header
    ws1[f"C{curr_row}"].fill = fill_dark_header
    ws1[f"C{curr_row}"].alignment = align_header
    ws1[f"C{curr_row}"].border = border_header
    ws1[f"D{curr_row}"].border = border_header
    ws1[f"E{curr_row}"].border = border_header

    ws1.merge_cells(f"F{curr_row}:G{curr_row}")
    ws1[f"F{curr_row}"] = "最終推奨方針"
    ws1[f"F{curr_row}"].font = font_header
    ws1[f"F{curr_row}"].fill = fill_dark_header
    ws1[f"F{curr_row}"].alignment = align_header
    ws1[f"F{curr_row}"].border = border_header
    ws1[f"G{curr_row}"].border = border_header
    ws1.row_dimensions[curr_row].height = 24

    flow_data = [
        (
            "パターン1（標準ケース）\n・Java 17以上を利用可能\n・Spring Boot 3系 or Jakarta EE 9+",
            "CXF 4.0と4.1は同じ「jakarta.*」パッケージ体系。Java 17 baselineを満たしているため、最も安全かつ自然にアップグレード可能。",
            "CXF 4.1.x にアップグレード\n【完全推奨 / コスト最小】"
        ),
        (
            "パターン2（Java 11縛りケース）\n・Java 11環境から直ちに引き上げられない\n・しかしjakarta.*名前空間は維持したい",
            "CXF 4.1はJDK 17必須のため直接移行不可。Javaランタイムを17に引き上げるか、商用サポート(Herodevs/TuxCare等)のNES利用を検討。",
            "JDK 17化と同時にCXF 4.1へ移行\n（または有償LTSサポートの検討）"
        ),
        (
            "パターン3（特殊レガシーケース）\n・実はシステム全体が Java EE 8 / javax.*\n・Spring Boot 2系から移行できていない",
            "CXF 4.0の採用検討自体が名前空間のミスマッチ。この場合のみ、javax.*互換を保つために3.6を採用することが「延命措置」として成立する。",
            "暫定的に CXF 3.6.x を採用\n（※ただし早期のJakarta移行計画が必須）"
        )
    ]

    curr_row += 1
    for i, row in enumerate(flow_data):
        ws1.row_dimensions[curr_row].height = 50
        fill_curr = fill_zebra_light if i % 2 == 1 else fill_white

        ws1.merge_cells(f"A{curr_row}:B{curr_row}")
        ws1[f"A{curr_row}"] = row[0]
        ws1[f"A{curr_row}"].font = font_data_bold
        ws1[f"A{curr_row}"].fill = fill_curr
        ws1[f"A{curr_row}"].alignment = align_left
        ws1[f"A{curr_row}"].border = border_cell
        ws1[f"B{curr_row}"].border = border_cell

        ws1.merge_cells(f"C{curr_row}:E{curr_row}")
        ws1[f"C{curr_row}"] = row[1]
        ws1[f"C{curr_row}"].font = font_data
        ws1[f"C{curr_row}"].fill = fill_curr
        ws1[f"C{curr_row}"].alignment = align_left
        ws1[f"C{curr_row}"].border = border_cell
        ws1[f"D{curr_row}"].border = border_cell
        ws1[f"E{curr_row}"].border = border_cell

        ws1.merge_cells(f"F{curr_row}:G{curr_row}")
        ws1[f"F{curr_row}"] = row[2]
        ws1[f"F{curr_row}"].font = font_data_bold
        ws1[f"F{curr_row}"].alignment = align_center
        ws1[f"F{curr_row}"].border = border_cell
        ws1[f"G{curr_row}"].border = border_cell
        if "完全推奨" in row[2]:
            ws1[f"F{curr_row}"].fill = fill_badge_recommended
            ws1[f"F{curr_row}"].font = font_badge_light
        elif "暫定" in row[2]:
            ws1[f"F{curr_row}"].fill = fill_badge_neutral
            ws1[f"F{curr_row}"].font = font_badge_light
        else:
            ws1[f"F{curr_row}"].fill = fill_badge_warning
            ws1[f"F{curr_row}"].font = font_badge_dark

        curr_row += 1

    # Deliberate column widths for Sheet 1
    ws1_widths = {'A': 18, 'B': 18, 'C': 34, 'D': 20, 'E': 28, 'F': 28, 'G': 26}
    for col_l, w in ws1_widths.items():
        ws1.column_dimensions[col_l].width = w
    apply_sheet_defaults(ws1)

    # =========================================================================
    # SHEET 2: バージョン比較・スペック一覧
    # =========================================================================
    ws2 = wb.create_sheet(title="バージョン比較・スペック一覧")
    ws2.freeze_panes = "A5"

    ws2.merge_cells("A1:E1")
    ws2["A1"] = "Apache CXF メジャー/マイナーバージョン詳細スペック比較表"
    ws2["A1"].font = font_title
    ws2["A1"].alignment = Alignment(horizontal='left', vertical='center')
    ws2.row_dimensions[1].height = 32

    ws2.merge_cells("A2:E2")
    ws2["A2"] = "※ CXF 3.6 (javax系最終), CXF 4.0 (EOL), CXF 4.1 (現行推奨), CXF 4.2 (次世代) の技術基盤マトリクス"
    ws2["A2"].font = font_subtitle
    ws2.row_dimensions[2].height = 18

    headers_ws2 = ["比較項目", "Apache CXF 3.6.x (javax延命)", "Apache CXF 4.0.x (EOL済)", "Apache CXF 4.1.x (現行推奨)", "Apache CXF 4.2.x (次世代)"]
    ws2.row_dimensions[4].height = 28
    for col_idx, text in enumerate(headers_ws2, 1):
        cell = ws2.cell(row=4, column=col_idx, value=text)
        cell.font = font_header
        cell.fill = fill_dark_header
        cell.alignment = align_header
        cell.border = border_header

    matrix_data = [
        ("ライフサイクル状態", "アクティブ保守中 (レガシー延命枠)", "【EOL (サポート終了)】", "【アクティブ保守中 (本命)】", "開発中 / 先進リリース"),
        ("EOL 到達日 / 最終版", "未定 (社区最終javax版として継続)", "2026年2月10日 (v4.0.11で終了)", "2027年以降 (長期メンテ予定)", "開発進行中 (将来標準)"),
        ("初回リリース年月", "2023年3月", "2022年12月", "2024年12月", "2025年末〜2026年"),
        ("パッケージ名前空間", "javax.* (Java EE 8互換)", "jakarta.* (Jakarta EE 9/10)", "jakarta.* (Jakarta EE 10)", "jakarta.* (Jakarta EE 11)"),
        ("必須 Java バージョン", "Java 11 以上", "Java 11 以上", "Java 17 以上 (LTS基準)", "Java 17 / 21 以上"),
        ("推奨 Java ランタイム", "Java 11 / Java 17", "Java 17", "Java 17 / Java 21", "Java 21 / 25"),
        ("Jakarta EE 準拠レベル", "Jakarta EE 8 (javax名前空間)", "Jakarta EE 9.1 (jakarta移行期)", "Jakarta EE 10 (本格普及版)", "Jakarta EE 11 (最新仕様)"),
        ("Spring Framework 対応", "Spring 5.3.x (Spring Boot 2系)", "Spring 6.0.x / 6.1.x", "Spring 6.2.x+ (Spring Boot 3.4+)", "Spring 6.x / 7.x"),
        ("Servlet 仕様ベースライン", "Servlet 4.0 / 3.1", "Servlet 5.0 / 6.0", "Servlet 6.0", "Servlet 6.1"),
        ("組込 HTTP エンジン", "Jetty 9 / 10, Tomcat 9", "Jetty 11, Tomcat 10.0", "Jetty 12 (ee10), Tomcat 10.1+", "Jetty 12, Tomcat 11"),
        ("JAX-WS / SOAP サポート", "完全対応 (javax.jws / javax.xml.ws)", "完全対応 (jakarta.jws / jakarta.xml.ws)", "完全対応 (jakarta.jws / jakarta.xml.ws)", "完全対応 (jakarta仕様準拠)"),
        ("JAX-RS / REST サポート", "完全対応 (javax.ws.rs.*)", "完全対応 (jakarta.ws.rs.*)", "完全対応 (jakarta.ws.rs.*)", "完全対応 (jakarta.ws.rs.*)"),
        ("最新 CVE 脆弱性パッチ", "公式パッチ提供あり (※javax系のみ)", "【提供なし (脆弱性放置リスク)】", "公式パッチ提供あり (迅速対応)", "公式パッチ提供あり"),
        ("新機能・仕様追加", "バグ修正・CVEパッチのみ", "完全停止 (クローズ)", "新機能・最新スタック統合継続", "新機能先行実装"),
        ("CXF 4.0からの移行難易度", "【極めて困難・高コスト】\n(全コードのimport/設定を逆変換)", "ー (現状維持はセキュリティ違反)", "【極めて容易・低コスト】\n(バージョン番号更新とJDK17適合)", "【中程度】\n(依存ライブラリの追従検証要)"),
        ("選定評価・推奨度", "△ 非推奨 (レガシー制約時のみ)", "× 採用不可 (EOL済)", "◎ 最有力推奨 (ベストチョイス)", "◯ 先進的検証用")
    ]

    curr_row = 5
    for i, row in enumerate(matrix_data):
        ws2.row_dimensions[curr_row].height = 36 if "\n" in row[1] or "\n" in row[4] else 24
        fill_curr = fill_zebra_light if i % 2 == 1 else fill_white

        for col_idx, val in enumerate(row, 1):
            cell = ws2.cell(row=curr_row, column=col_idx, value=val)
            cell.fill = fill_curr
            cell.border = border_cell
            if col_idx == 1:
                cell.font = font_data_bold
                cell.alignment = align_left
            elif col_idx in [2, 3, 4, 5]:
                cell.alignment = align_center
                if "EOL" in val or "不可" in val:
                    cell.font = font_data_bold
                elif "◎" in val:
                    cell.font = font_badge_light
                    cell.fill = fill_badge_recommended
                elif "×" in val:
                    cell.font = font_badge_dark
                    cell.fill = fill_badge_danger
                elif "△" in val:
                    cell.font = font_badge_dark
                    cell.fill = fill_badge_warning
                else:
                    cell.font = font_data
        curr_row += 1

    ws2_widths = {'A': 26, 'B': 34, 'C': 34, 'D': 34, 'E': 30}
    for col_l, w in ws2_widths.items():
        ws2.column_dimensions[col_l].width = w
    apply_sheet_defaults(ws2)

    # =========================================================================
    # SHEET 3: 方針別メリット・デメリット評価
    # =========================================================================
    ws3 = wb.create_sheet(title="方針別メリット・デメリット評価")
    ws3.freeze_panes = "A5"

    ws3.merge_cells("A1:D1")
    ws3["A1"] = "CXF 4.0 EOL対応 方針別多角評価マトリクス"
    ws3["A1"].font = font_title
    ws3.row_dimensions[1].height = 32

    ws3.merge_cells("A2:D2")
    ws3["A2"] = "※ ご質問の「3.6回帰案」、現状維持の「4.0放置案」、推奨の「4.1アップグレード案」を6軸で徹底比較"
    ws3["A2"].font = font_subtitle
    ws3.row_dimensions[2].height = 18

    headers_ws3 = ["評価軸 / 観点", "方針A: CXF 4.0 そのまま利用 (現状維持)", "方針B: CXF 3.6 へ回帰 (ご質問の検討案)", "方針C: CXF 4.1 へ移行 (強く推奨)"]
    ws3.row_dimensions[4].height = 28
    for col_idx, text in enumerate(headers_ws3, 1):
        cell = ws3.cell(row=4, column=col_idx, value=text)
        cell.font = font_header
        cell.fill = fill_dark_header
        cell.alignment = align_header
        cell.border = border_header

    eval_data = [
        (
            "基本方針と狙い",
            "EOLを迎えた4.0.11を改修せずそのまま稼働させ続ける。",
            "「3.6はまだ保守されている」という理由で、1世代前の3.6系へダウングレードする。",
            "直系後継である4.1系にバージョンアップし、最新のセキュリティと仕様に追従する。"
        ),
        (
            "妥当性判定",
            "【不当・重大リスク】",
            "【非妥当・技術的アンチパターン】",
            "【極めて妥当・ベストプラクティス】"
        ),
        (
            "セキュリティ面のリスク\n(CVE脆弱性対応)",
            "【致命的】\n2026年2月以降に発見された新たな脆弱性（XXE、SSRF、DoS等）に対してパッチが一切提供されない。監査・セキュリティ審査に不合格となる。",
            "【一時的延命に過ぎない】\n現在はパッチが出るが、コミュニティはいずれ3.6のEOLも迎える。将来再び同じEOL問題に直面する。",
            "【極めて安全】\nコミュニティの最前線でアクティブにCVEパッチが供給される。商用環境でのコンプライアンス要件を完全にクリア可能。"
        ),
        (
            "ソースコード・改修工数\n(マイグレーションコスト)",
            "【ゼロ】\n何もしないため短期的工数は発生しない（ただし事故発生時の損失は青天井）。",
            "【莫大な改修コスト (逆行)】\n・全Javaソースの jakarta.* を javax.* に書き戻し\n・Spring Boot 3から2へのダウングレード、あるいは特殊なブリッジ設定が必要となり工数が爆発。",
            "【極めて軽微 (最小工数)】\n・同じ jakarta.* のためコード修正はほぼ不要\n・pom.xml / build.gradle のバージョン番号更新とJDK 17動作確認のみで完了。"
        ),
        (
            "エコシステム互換性\n(Spring Boot / サーバー)",
            "Spring Boot 3.0〜3.2と互換はあるが、Spring側のEOLや依存関係の乖離が進み徐々に壊れる。",
            "【完全崩壊】\nSpring Boot 3.xやTomcat 10+、Jetty 12等と衝突。javaxを使うために古い基盤への退行を余儀なくされる。",
            "【完全適合】\nSpring Boot 3.3 / 3.4+、Jetty 12、Hibernate 6.6など、最新のエンタープライズ基盤とネイティブに適合。"
        ),
        (
            "アーキテクチャ将来性\n(技術的負債)",
            "負債が急激に腐敗。外部連携先からのセキュリティ要請に応えられなくなる。",
            "【最悪の負債再抱え込み】\n業界標準が「Jakarta EE」に完全移行している中、自ら過去の「Java EE 8 (javax)」に飛び込むため、将来の再移行コストが倍増する。",
            "【健全な資産化】\nJakarta EE 10 / JDK 17の現代標準に乗ることで、今後5年〜10年の安定運用基盤が確立される。"
        ),
        (
            "総合評価・結論",
            "即時停止すべき。放置は企業のコンプライアンス違反・インシデント直結。",
            "【絶対に避けるべき悪手】\n「3.6が保守中」という表面的な事実だけで選ぶと、アーキテクチャの破綻を招く。",
            "【唯一無二の正解】\n4.0を利用していたプロジェクトであれば、迷わず4.1へステップアップすべきである。"
        )
    ]

    curr_row = 5
    for i, row in enumerate(eval_data):
        ws3.row_dimensions[curr_row].height = 58 if "\n" in row[2] or "\n" in row[3] else 28
        fill_curr = fill_zebra_light if i % 2 == 1 else fill_white

        for col_idx, val in enumerate(row, 1):
            cell = ws3.cell(row=curr_row, column=col_idx, value=val)
            cell.fill = fill_curr
            cell.border = border_cell
            if col_idx == 1:
                cell.font = font_data_bold
                cell.alignment = align_left
            elif col_idx == 2:
                cell.alignment = align_left
                cell.font = font_data
                if "致命的" in val or "不当" in val:
                    cell.fill = fill_badge_danger
                    cell.font = font_badge_dark
            elif col_idx == 3:
                cell.alignment = align_left
                cell.font = font_data
                if "非妥当" in val or "絶対に避けるべき" in val:
                    cell.fill = fill_badge_warning
                    cell.font = font_badge_dark
            elif col_idx == 4:
                cell.alignment = align_left
                cell.font = font_data
                if "ベストプラクティス" in val or "正解" in val:
                    cell.fill = fill_badge_recommended
                    cell.font = font_badge_light
        curr_row += 1

    ws3_widths = {'A': 24, 'B': 38, 'C': 42, 'D': 42}
    for col_l, w in ws3_widths.items():
        ws3.column_dimensions[col_l].width = w
    apply_sheet_defaults(ws3)

    # =========================================================================
    # SHEET 4: CXF内部動作原理・Phase一覧
    # =========================================================================
    ws4 = wb.create_sheet(title="CXF内部動作原理・Phase一覧")
    ws4.freeze_panes = "A6"

    ws4.merge_cells("A1:F1")
    ws4["A1"] = "Apache CXF の心臓部：PhaseInterceptorChain 動作パイプライン完全解説"
    ws4["A1"].font = font_title
    ws4.row_dimensions[1].height = 32

    ws4.merge_cells("A2:F2")
    ws4["A2"] = "※ メッセージ送受信時にインターセプターが実行される全フェーズ順序と、各フェーズの具体的な役割"
    ws4["A2"].font = font_subtitle
    ws4.row_dimensions[2].height = 18

    # Inbound Section
    ws4.merge_cells("A4:F4")
    ws4["A4"] = "【受信チェーン：Inbound Message Processing (全15フェーズ順)】 〜 HTTPリクエストからJavaメソッド呼出まで 〜"
    ws4["A4"].font = font_section
    ws4["A4"].fill = fill_section
    ws4["A4"].alignment = Alignment(horizontal='left', vertical='center', indent=1)
    ws4.row_dimensions[4].height = 24

    headers_phase = ["順序", "フェーズ定数名 (Phase)", "フェーズ概要・分類", "詳細な動作内容と処理メカニズム", "代表的なビルトインInterceptor", "小学生向けイメージ（ベルトコンベア）"]
    ws4.row_dimensions[5].height = 26
    for col_idx, text in enumerate(headers_phase, 1):
        cell = ws4.cell(row=5, column=col_idx, value=text)
        cell.font = font_header
        cell.fill = fill_dark_header
        cell.alignment = align_header
        cell.border = border_header

    inbound_phases = [
        ("1", "Phase.RECEIVE", "トランスポート受信", "ネットワーク経由（HTTP/JMS等）で生データを受信し、CXFメッセージオブジェクトに格納する。", "AttachmentInInterceptor", "トラックから荷物の箱を降ろして作業台に置く"),
        ("2", "Phase.PRE_STREAM", "ストリーム前処理", "受信バイトストリームの読み込み直前に行う事前処理。復号化や解凍の準備。", "CertConstraintsInterceptor", "箱の伝票や施錠状態をざっと確認する"),
        ("3", "Phase.STREAM", "ストリーム変換", "GZIPの解凍や、ストリームレベルでの暗号復号処理を実行する。", "GZIPInInterceptor", "ビニール袋を破いて中身の束を取り出す"),
        ("4", "Phase.POST_STREAM", "ストリーム後処理", "ストリーム変換完了後の検証やログ出力を行う。", "LoggingInInterceptor", "何重に包まれていたか作業記録をつける"),
        ("5", "Phase.READ", "メッセージ読込", "XMLパーサー（StAX）を初期化し、XMLヘッダーや開始タグを読み込む。", "StaxInInterceptor", "ハサミで手紙の封筒の口をチョキチョキ切る"),
        ("6", "Phase.PRE_PROTOCOL", "プロトコル前処理", "SOAPバージョン（1.1 / 1.2）の判定や、JAX-RSリソースの事前照合。", "MEXInInterceptor", "手紙が日本語か英語か、形式をチェックする"),
        ("7", "Phase.PROTOCOL", "プロトコル処理", "SOAP Envelope / Header を解析し、WS-Security署名検証や暗号解読を実行。", "WSS4JInInterceptor, SoapHeaderInterceptor", "南京錠を開け、手紙の差出人印鑑が本物か確かめる"),
        ("8", "Phase.POST_PROTOCOL", "プロトコル後処理", "プロトコルヘッダー処理後のクリーンアップや必須ヘッダー（mustUnderstand）の検証。", "MustUnderstandInterceptor", "「必ず読んでね」という重要シールを確認する"),
        ("9", "Phase.UNMARSHAL", "データ復元 (脱直列化)", "JAXBバインディングを用い、XML/JSONテキストをJavaオブジェクトに変換・復元する。", "DocLiteralInInterceptor, JAXBDataBinding", "手紙の文章を読んで、コンピュータが理解できる電子データに入力する"),
        ("10", "Phase.PRE_LOGICAL", "論理処理前", "オブジェクト復元完了後、ビジネスロジック実行前の検証やセキュリティ権限チェック。", "SimpleAuthorizingInterceptor", "この人が注文して良い権限を持っているか会員名簿と照らし合わせる"),
        ("11", "Phase.LOGICAL", "論理ハンドラ処理", "JAX-WSのLogicalHandlerを実行し、メッセージボディの内容を検査・加工する。", "LogicalHandlerInInterceptor", "注文内容に記入漏れがないかチェックする"),
        ("12", "Phase.POST_LOGICAL", "論理処理後", "論理ハンドラ処理完了後のメッセージ整形・コンテキスト確定。", "WrapperClassInInterceptor", "注文データをシェフ（担当者）のお皿に盛り付ける"),
        ("13", "Phase.PRE_INVOKE", "呼出直前準備", "実行対象のJavaサービスエンドポイント（Bean）やメソッド引数の最終バインド。", "HolderInInterceptor", "シェフの前に「注文票」を差し出す"),
        ("14", "Phase.INVOKE", "サービス呼出 (実行)", "実際のビジネスロジック（Javaメソッド）を実行し、戻り値を受け取る。", "ServiceInvokerInterceptor", "シェフが実際に料理を作り上げる（Java実行！）"),
        ("15", "Phase.POST_INVOKE", "呼出後処理", "メソッド完了後のトランザクションコミット準備やOutboundチェーンの起動トリガー。", "OutgoingChainInterceptor", "出来上がった料理を配膳トレイに乗せる")
    ]

    curr_row = 6
    for i, row in enumerate(inbound_phases):
        ws4.row_dimensions[curr_row].height = 26
        fill_curr = fill_zebra_light if i % 2 == 1 else fill_white

        for col_idx, val in enumerate(row, 1):
            cell = ws4.cell(row=curr_row, column=col_idx, value=val)
            cell.fill = fill_curr
            cell.border = border_cell
            if col_idx == 1:
                cell.alignment = align_center
                cell.font = font_data_bold
            elif col_idx == 2:
                cell.alignment = align_left
                cell.font = font_data_bold
            elif col_idx == 3:
                cell.alignment = align_center
                cell.font = font_data
            elif col_idx in [4, 5, 6]:
                cell.alignment = align_left
                cell.font = font_data
        curr_row += 1

    # Outbound Section
    curr_row += 2
    ws4.merge_cells(f"A{curr_row}:F{curr_row}")
    ws4[f"A{curr_row}"] = "【送信チェーン：Outbound Message Processing (全11フェーズ順)】 〜 Javaの戻り値からHTTPレスポンス返信まで 〜"
    ws4[f"A{curr_row}"].font = font_section
    ws4[f"A{curr_row}"].fill = fill_section
    ws4[f"A{curr_row}"].alignment = Alignment(horizontal='left', vertical='center', indent=1)
    ws4.row_dimensions[curr_row].height = 24

    curr_row += 1
    ws4.row_dimensions[curr_row].height = 26
    for col_idx, text in enumerate(headers_phase, 1):
        cell = ws4.cell(row=curr_row, column=col_idx, value=text)
        cell.font = font_header
        cell.fill = fill_dark_header
        cell.alignment = align_header
        cell.border = border_header

    outbound_phases = [
        ("1", "Phase.SETUP", "初期化準備", "Outboundチェーン全体のコンテキスト初期化、レスポンスヘッダーの設定。", "ClientRequestFilter (JAX-RS)", "新しい返信用封筒を用意する"),
        ("2", "Phase.PRE_LOGICAL", "論理前処理", "オブジェクトシリアライズ前の共通メタデータ設定。", "HolderOutInterceptor", "返信のお手紙に日付と宛名を書く"),
        ("3", "Phase.LOGICAL", "論理ハンドラ処理", "JAX-WS LogicalHandler による出力オブジェクトの事前検査・加工。", "LogicalHandlerOutInterceptor", "手紙の内容に失礼な点がないか確認する"),
        ("4", "Phase.POST_LOGICAL", "論理後処理", "論理加工完了後の最終調整。", "WrapperClassOutInterceptor", "手紙をきれいに三つ折りにする"),
        ("5", "Phase.WRITE", "プロトコル書込開始", "SOAP Envelope / Header のXMLタグ書き込みを開始（StAX Writer起動）。", "SoapOutInterceptor", "封筒の表面にSOAPというスタンプを押す"),
        ("6", "Phase.MARSHAL", "データ直列化", "Javaオブジェクト（戻り値）をXML/JSONテキストに変換してXMLストリームへ出力。", "DataBindingSerializer (JAXB)", "日本語の文章をXMLという世界共通の言葉に翻訳して書く"),
        ("7", "Phase.PREPARE_SEND", "接続・送信準備", "HTTP接続（Conduit）を確立し、ヘッダー（Content-Type等）を設定する。", "HTTPConduit, MessageSenderInterceptor", "郵便屋さんに電話して集荷の予約をする"),
        ("8", "Phase.PRE_STREAM", "ストリーム前処理", "WS-SecurityによるXML署名付与や暗号化の適用。", "WSS4JOutInterceptor", "手紙に差出人の印鑑を押し、大切な部分に鍵をかける"),
        ("9", "Phase.STREAM", "ストリーム圧縮・暗号", "GZIP圧縮やバイト単位のフィルタリングを実行。", "GZIPOutInterceptor", "手紙をぎゅっと圧縮して小さなカプセルに入れる"),
        ("10", "Phase.POST_STREAM", "ストリーム完了処理", "XMLストリームのフラッシュ、書き込み完了通知。", "AttachmentOutInterceptor", "カプセルをしっかり閉める"),
        ("11", "Phase.SEND", "トランスポート送出", "ソケットを通じて相手へバイト列を送信し、コネクションを閉じる/維持する。", "WrappedOutputStream, HTTP Transport", "郵便屋さんのバイクに乗せて相手へ出発！")
    ]

    curr_row += 1
    for i, row in enumerate(outbound_phases):
        ws4.row_dimensions[curr_row].height = 26
        fill_curr = fill_zebra_light if i % 2 == 1 else fill_white

        for col_idx, val in enumerate(row, 1):
            cell = ws4.cell(row=curr_row, column=col_idx, value=val)
            cell.fill = fill_curr
            cell.border = border_cell
            if col_idx == 1:
                cell.alignment = align_center
                cell.font = font_data_bold
            elif col_idx == 2:
                cell.alignment = align_left
                cell.font = font_data_bold
            elif col_idx == 3:
                cell.alignment = align_center
                cell.font = font_data
            elif col_idx in [4, 5, 6]:
                cell.alignment = align_left
                cell.font = font_data
        curr_row += 1

    ws4_widths = {'A': 8, 'B': 24, 'C': 22, 'D': 48, 'E': 36, 'F': 38}
    for col_l, w in ws4_widths.items():
        ws4.column_dimensions[col_l].width = w
    apply_sheet_defaults(ws4)

    # =========================================================================
    # SHEET 5: 移行作業チェックリスト
    # =========================================================================
    ws5 = wb.create_sheet(title="移行作業チェックリスト")
    ws5.freeze_panes = "A5"

    ws5.merge_cells("A1:G1")
    ws5["A1"] = "CXF 4.0 → 4.1 アップグレード移行 実務タスクチェックリスト"
    ws5["A1"].font = font_title
    ws5.row_dimensions[1].height = 32

    ws5.merge_cells("A2:G2")
    ws5["A2"] = "※ CXF 4.1への安全な移行を完遂するためのステップ別作業項目、検証方法、およびリスク対策"
    ws5["A2"].font = font_subtitle
    ws5.row_dimensions[2].height = 18

    headers_ws5 = ["No.", "作業フェーズ", "タスク項目", "対象レイヤー / ファイル", "具体的な作業内容・コード改修ポイント", "完了検証基準 (Definition of Done)", "推奨ステータス"]
    ws5.row_dimensions[4].height = 28
    for col_idx, text in enumerate(headers_ws5, 1):
        cell = ws5.cell(row=4, column=col_idx, value=text)
        cell.font = font_header
        cell.fill = fill_dark_header
        cell.alignment = align_header
        cell.border = border_header

    tasks_data = [
        ("1", "前提条件確認", "JDKバージョンの確認", "Dockerfile, CI/CD, pom.xml", "プロジェクトの実行環境およびビルド環境が JDK 17 以上であることを確認（CXF 4.1の必須要件）。", "java -version が 17/21 を返却し、mvn clean compile が通ること", "必須"),
        ("2", "依存関係更新", "CXFバージョン定義の更新", "pom.xml / build.gradle", "<cxf.version>4.0.x</cxf.version> を <cxf.version>4.1.0</cxf.version> (または最新4.1.x) に書き換え。", "mvn dependency:tree で 4.1.x 系アーティファクトのみが解決されること", "必須"),
        ("3", "依存関係更新", "Spring Boot / Framework 整合", "pom.xml / build.gradle", "Spring Boot 3.3.x または 3.4.x 系と cxf-spring-boot-starter-jaxws / jaxrs のバージョン互換を確認。", "ビルドエラーなくSpring ApplicationContextが正常起動すること", "必須"),
        ("4", "ビルドプラグイン", "cxf-codegen-plugin 更新", "pom.xml (WSDL2Java)", "WSDLからJavaコードを自動生成する cxf-codegen-plugin を 4.1.x に更新し、Java 17構文に対応。", "mvn generate-sources でWSDLからスタブコードが正常再生成されること", "必須"),
        ("5", "コード確認", "Jakarta EE アノテーション検証", "Java ソースコード全般", "CXF 4.0で既に jakarta.* を利用しているため原則変更不要だが、非推奨メソッドや削除クラスの有無を点検。", "コンパイラ警告/エラーがゼロであること", "確認"),
        ("6", "コード確認", "カスタムInterceptorの確認", "AbstractPhaseInterceptor 実装クラス", "自作Interceptorが存在する場合、handleMessage() 内で利用している内部APIが4.1で変更されていないか確認。", "単体テストでカスタムInterceptorが期待通りフェーズ実行されること", "確認"),
        ("7", "セキュリティ", "依存ライブラリ脆弱性スキャン", "プロジェクト全体", "OWASP Dependency-Check または Snyk / Trivy を実行し、既知のCVE（特に4.0に残存したCVE）が解消されたか検証。", "高重大度(Critical/High)の脆弱性が検出されないこと", "必須"),
        ("8", "テスト・検証", "SOAP/REST 通信の結合テスト", "E2Eテスト / Postman / SoapUI", "代表的なSOAPリクエスト（正常系、異常系SOAP Fault、WS-Security署名検証）およびRESTエンドポイントを実行。", "全HTTPステータスおよびXML/JSONペイロードが4.0時代と同一に動作すること", "必須"),
        ("9", "本番配備", "ステージング・カナリア検証", "インフラ / K8s / APサーバー", "本番相当のステージング環境で負荷テスト（JMeter等）を実施し、メモリリークやスレッド滞留がないことを確認。", "レイテンシ、スループット、エラー率に退行(Regression)がないこと", "完了後リリース")
    ]

    curr_row = 5
    for i, row in enumerate(tasks_data):
        ws5.row_dimensions[curr_row].height = 34
        fill_curr = fill_zebra_light if i % 2 == 1 else fill_white

        for col_idx, val in enumerate(row, 1):
            cell = ws5.cell(row=curr_row, column=col_idx, value=val)
            cell.fill = fill_curr
            cell.border = border_cell
            if col_idx == 1:
                cell.alignment = align_center
                cell.font = font_data_bold
            elif col_idx in [2, 7]:
                cell.alignment = align_center
                cell.font = font_data_bold
                if val == "必須":
                    cell.fill = fill_badge_danger
                    cell.font = font_badge_dark
                elif val == "確認":
                    cell.fill = fill_badge_neutral
                    cell.font = font_badge_light
                elif "リリース" in val:
                    cell.fill = fill_badge_recommended
                    cell.font = font_badge_light
            elif col_idx in [3, 4]:
                cell.alignment = align_left
                cell.font = font_data_bold
            elif col_idx in [5, 6]:
                cell.alignment = align_left
                cell.font = font_data
        curr_row += 1

    ws5_widths = {'A': 6, 'B': 16, 'C': 28, 'D': 26, 'E': 48, 'F': 44, 'G': 16}
    for col_l, w in ws5_widths.items():
        ws5.column_dimensions[col_l].width = w
    apply_sheet_defaults(ws5)

    output_filename = "Apache_CXF_Version_Evaluation_Matrix.xlsx"
    wb.save(output_filename)

    # Post-process zip to guarantee Font 0 in styles.xml is Meiryo UI
    import zipfile, shutil
    temp_filename = output_filename + ".tmp"
    with zipfile.ZipFile(output_filename, 'r') as zin, zipfile.ZipFile(temp_filename, 'w') as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'xl/styles.xml':
                data = data.replace(b'val="Calibri"', b'val="Meiryo UI"')
            zout.writestr(item, data)
    shutil.move(temp_filename, output_filename)
    print(f"Successfully generated refined: {output_filename}")

if __name__ == "__main__":
    build_cxf_excel()
