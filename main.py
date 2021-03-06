import scipy.io.wavfile                 # WAVファイルを読み込むために使用
from scipy import signal                # 極大値を求めるために使用
import numpy as np                      # データの整形や高速フーリエ変換に使用
import pandas as pd                     # ピアノの音階辞書を作成するために使用
import matplotlib.pyplot as plt         # 図の作成に使用
import matplotlib.animation as anm      # アニメーション作成に使用
import matplotlib.patches as pat        # 長方形を描画するために使用
import time                             # 時間を表示するために使用

#音声ファイル読み込み
wav_filename = "./source.wav"
rate, data = scipy.io.wavfile.read(wav_filename) # サンプリング周波数とデータ

print("サンプリング周波数:", rate)
print("データ数:", len(data))

if data.ndim < 2:    # 配列の次元数
    print("モノラル")
else:
    print("ステレオ")
    # 連結して偶数要素を抽出する
    data = np.ravel(data)[::2]
print(data)

# 振幅の配列を作成 (-1 から 1 に正規化)
data = data / 32768

# データを分割 0.1秒ごと
split_datas = np.array_split(data, int(len(data) / (rate * 0.1)))
print("分割数:", len(split_datas))

count = 0
ex_freqency = []    # 抽出したデータを格納するために用意
for short_data in split_datas:
    ex_freqency.append([])    # データを格納するために空リストを追加
    # フーリエ変換により周波数成分と振幅を取得
    fft_short_data = np.abs(np.fft.fft(short_data))    
    freqList = np.fft.fftfreq(short_data.shape[0], d=1.0/rate)

    maxid = signal.argrelmax(fft_short_data, order=2)    # 極大値を求める
    for i in maxid[0]:
        if fft_short_data[i] > 10 and 25 < freqList[i] < 4200:
            ex_freqency[count].append(freqList[i])    # 周波数を格納
    count += 1

piano_dic = pd.read_csv("./piano_dict.csv", encoding="utf-8")
print(piano_dic)

black_keys = piano_dic[piano_dic["scaleNameEn"].str.contains("#")].index
print(black_keys)

count = 0
keys = [] # 含まれる周波数の行
for row in ex_freqency:
    keys.append([])    # 各フレームの周波数を格納するために空リストを追加
    for i in row:
        key = piano_dic.loc[abs(piano_dic.frequency - i).idxmin(), "keyNumber"]    # 差が最小の音階
        if (key in keys[count]) == False:
            keys[count].append(key)    # かぶってなければ音階を追加
    count += 1
print(keys)

fig, ax = plt.subplots(figsize = (10, 2))

# 各フレームの描画
def update(i, fig_title, data_list, ax):
    if i != 0:
        plt.cla()    # 現在描写されているグラフを消去
    ax.axis("off")    # 軸と目盛りを削除
    ax.set_xlim(0, 52.1)
    ax.set_ylim(-0.5, 2.5)
    skip = False
    white_count = 0
    plt.title(fig_title + time.strftime("%M:%S", time.gmtime(i * 0.1)))
    for j in range(0, 88):
        if skip == True:
            skip = False    # フラグをおろす
            continue    # 既に描画した白鍵をスキップする
        if j in black_keys:
            # 黒鍵の右側の白鍵を描画
            color = "white"
            if j + 1 in data_list[i]:
                color = "red"    # 音が鳴っていれば色を赤にする
            rec = pat.Rectangle(xy = (white_count, 0), width = 1, height = 1.5, fc = color, ec = "black")    # 長方形を作成
            ax.add_patch(rec)    # Axesに長方形を追加
            skip = True    # スキップフラグをたてる
            # 白鍵の上に黒鍵を描画
            color = "gray"
            x, y = white_count - 0.3, 0.5
            w, h = 0.6, 1
        else:
            # 白鍵を描画
            color = "white"
            x, y = white_count, 0
            w, h = 1, 1.5
        if j in data_list[i]:
            color = "red"    # 音が鳴っていれば色を赤にする
        rec = pat.Rectangle(xy = (x, y), width = w, height = h, fc = color, ec = "black")    # 長方形を作成
        ax.add_patch(rec)    # Axesに長方形を追加
        white_count += 1    # 白鍵の数をカウント

# アニメーションを生成
ani = anm.FuncAnimation(fig, update, fargs=("Mimicopy ", keys, ax), interval=100, frames=len(keys))
# gifファイルとして保存
ani.save("Sample.gif", writer="pillow")
