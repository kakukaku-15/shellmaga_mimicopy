ここでは、「シェルスクリプトマガジン Vol.69の香川大学SLPからお届け！」で、
紹介したプログラムをアップロードしています。
使用した音声ファイルやCSVファイルも置いていますので、自由にお使いください。

# はじめに

耳コピを支援するためのプログラムを作成しました。

# 開発環境

- Python 3.7.4 

# ファイル

- piano_dict.csv
    - ピアノの音階辞書を作成するためのCSVファイル
- sample.wav
    - 読み込む音声ファイル
    - きらきら星変奏曲 一部抜粋
- mimicopy.py
    - 音声ファイルをピアノの鍵盤で可視化するプログラム

# 仕様

1. WAVファイルを読み込み
    - ステレオならば、連結して偶数要素を抽出
    - モノラルならば、そのまま
2. 0.1秒ごとにデータを分割し、配列に格納
3. 高速フーリエ変換により、周波数成分と振れ幅を取得
    - 88鍵ピアノの音域である帯域の周波数だけを抽出
4. ピアノの音階の辞書を作成
5. 辞書より、一番近い周波数の音階番号を取得
6. 可視化
    - MatplotLibで長方形を描画
    - 音声ファイルより抽出した音の鍵盤の色は赤くして表示
