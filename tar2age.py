import os
import subprocess
from pathlib import Path

def encrypt_existing_archives(
    source_dir: str, 
    output_dir: str, 
    recipient_key: str, 
    archive_extensions: tuple = (".zip", ".tar", ".gz", ".7z", ".tgz", ".bz2")
):
    """
    指定ディレクトリ内にある既存のアーカイブファイルを検索し、
    ageで暗号化して出力ディレクトリへ書き出す
    """
    source_path = Path(source_dir).resolve()
    out_path = Path(output_dir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)
    
    print(f"アーカイブ検索元: {source_path}")
    
    # 指定された拡張子を持つファイルのみを抽出
    archive_files = [
        p for p in source_path.iterdir() 
        if p.is_file() and p.suffix.lower() in archive_extensions
    ]
    
    if not archive_files:
        print("対象となるアーカイブファイルが見つかりませんでした。")
        return
        
    print(f"見つかったアーカイブ数: {len(archive_files)} 件\n")
    
    for arc_path in sorted(archive_files):
        # 出力ファイル名（例: backup.zip -> backup.zip.age）
        age_path = out_path / f"{arc_path.name}.age"
        
        print(f"暗号化中: {arc_path.name} -> {age_path.name}")
        
        # ageコマンドの実行 (-r: 公開鍵指定, パスフレーズの場合は -p に変更可能)
        cmd = ["age", "-r", recipient_key, "-o", str(age_path), str(arc_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"  [エラー] {arc_path.name} の暗号化に失敗しました: {result.stderr.strip()}")
        else:
            print(f"  [成功] 完了しました")

    print("\nすべてのアーカイブの暗号化処理が完了しました！")

# --- 実行設定の例 ---
if __name__ == "__main__":
    # 7-Zip等で事前にアーカイブを作成したフォルダを指定
    SOURCE_DIRECTORY = "./archives"      
    # 暗号化したファイルを書き出す出力先フォルダ
    OUTPUT_DIRECTORY = "./encrypted" 
    # あなたのage公開鍵（パスフレーズ運用にする場合は -p を使うようcmdを変更）
    RECIPIENT_PUBLIC_KEY = "age1v9fkzx479yr53wlx9e0pesk00usupezp0cyx5v9znzdy7rqurq7qa479me" 
    
    encrypt_existing_archives(
        source_dir=SOURCE_DIRECTORY,
        output_dir=OUTPUT_DIRECTORY,
        recipient_key=RECIPIENT_PUBLIC_KEY
    )