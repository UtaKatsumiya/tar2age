from pathlib import Path
import subprocess
import sys

# --- 設定項目 ---
# 秘密鍵ファイルのパス（identity file）
KEY_FILE = Path("../../documents/password/age/key.txt")

# 暗号化されたファイルが格納されているフォルダのパス
ENCRYPTED_DIR = Path(__file__).resolve().parent / "encrypted"

# 復号したファイルの出力先フォルダのパス
OUTPUT_DIR = Path(__file__).resolve().parent / "decrypted"
# ----------------

def main():
    # 1. 存在確認
    if not KEY_FILE.is_file():
        print(f"エラー: 秘密鍵ファイルが見つかりません: {KEY_FILE}", file=sys.stderr)
        sys.exit(1)

    if not ENCRYPTED_DIR.is_dir():
        print(f"エラー: 暗号化フォルダが見つかりません: {ENCRYPTED_DIR}", file=sys.stderr)
        sys.exit(1)

    # 出力先フォルダが存在しない場合は自動作成
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=== ageによる ファイルの一括復号を開始します ===")
    print(f"秘密鍵: {KEY_FILE}")
    print(f"入力元: {ENCRYPTED_DIR}")
    print(f"出力先: {OUTPUT_DIR}\n")

    # 2. 指定フォルダ以下のすべての .age ファイルを再帰的に検索
    for file_path in ENCRYPTED_DIR.rglob("*.age"):
        if file_path.is_file():
            # サブフォルダの階層構造を保持した相対パスを計算
            relative_path = file_path.relative_to(ENCRYPTED_DIR)
            
            # 末尾の ".age" を取り除いたファイル名を出力先とする（例: note.md.age -> note.md）
            output_file = OUTPUT_DIR / relative_path.with_suffix("")
            
            # 出力先のサブフォルダが存在しない場合は作成
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            print(f"復号中: {file_path} -> {output_file}")
            
            try:
                # ageコマンドの実行 (-i: 秘密鍵を指定, -d: 復号モード)
                subprocess.run(
                    ["age", "-d", "-i", str(KEY_FILE), "-o", str(output_file), str(file_path)],
                    check=True
                )
                
            except subprocess.CalledProcessError as e:
                print(f"エラー: ファイルの復号に失敗しました: {file_path} (詳細: {e})", file=sys.stderr)
            except FileNotFoundError:
                print("エラー: `age` コマンドがシステムに見つかりません。ageがインストールされているか確認してください。", file=sys.stderr)
                sys.exit(1)

    print("\n=== すべてのファイルの復号が完了しました ===")

if __name__ == "__main__":
    main()