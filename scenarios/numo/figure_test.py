import numpy as np
import matplotlib.pyplot as plt
import imageio
import csv

OVER_SIZE_LIMIT = 200_000_000

csv.field_size_limit(OVER_SIZE_LIMIT)



# パラメータ設定
num_subcarriers = 3  # サブキャリア数（周波数方向）
num_slot = 50    # OFDMシンボル数（時間方向）
num_frames = 200       # GIFのフレーム数

# GIF用フレームのリスト
frames = []



# GIFを作成するループ
for frame_idx in range(num_frames):
    # ランダムなリソースグリッドを生成
    resource_grid = np.random.rand(num_subcarriers,num_slot)

    # プロットの作成
    fig, ax = plt.subplots(figsize=(16, 6))
    im = ax.imshow(resource_grid, aspect=5, cmap='viridis', origin='lower')
    ax.set_title(f"Frame {frame_idx + 1}")
    ax.set_xlabel("Subcarriers (Frequency)")
    ax.set_ylabel("OFDM Symbols (Time)")
    fig.colorbar(im, ax=ax, orientation='vertical', label="Amplitude")
    
    # フレーム内にテキストを追加
    for i in range(num_subcarriers):
        for j in range(num_slot):
            ax.text(j, i, f"{resource_grid[i, j]:.1f}", 
                    ha='center', va='center', color='white', fontsize=6)
    
    # 図を一時的に保存してフレームに追加
    filename = f"frame_{frame_idx}.png"
    plt.savefig(filename)
    frames.append(imageio.imread(filename))
    plt.close(fig)

# GIFの保存
output_gif = "resource_grid_animation.gif"
imageio.mimsave(output_gif, frames, duration=0.8)  # 0.5秒間隔でフレームを結合

print(f"GIFが保存されました: {output_gif}")