import sys
# ファイル名を指定
file_name = "../../build/ds_memo.txt"
args = sys.argv
if len(args) >3:
    file_name = args[1]

# フィルタリングした行を格納するリスト
filtered_lines = []

# ファイルを読み込む
with open(file_name, "r", encoding="utf-8") as file:
    for line in file:
        # 改行を除去
        line = line.strip()
        
        # "!sent"を含む行を確認
        if "!sent" in line:
            # 行を","で分割
            parts = line.split(",")
            if len(parts) > 0:  # partsが空でないことを確認
                try:
                    # 最初の要素を数値としてチェック
                    if float(parts[0]) >= 200:
                        filtered_lines.append(line)
                except ValueError:
                    # 最初の要素が数値でない場合はスキップ
                    continue

# 結果を表示
print(filtered_lines[0:10])
print(len(filtered_lines))