import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import csv
import os

# ====================== 【全局配置】自动清空CSV ======================
CSV_FILE = "有效拟合星系结果.csv"
# 完全匹配你的表头！一个字都不差
HEADERS = [
    "星系名称", "总重子质量(M⊙)", "η((km/s)²)", "r0(kpc)", "r1(kpc)", "alpha", "beta", "拟合优度R²"
]

def auto_clear_and_init_csv():
    """
    自动清空旧数据，只保留表头
    运行时自动执行，不用手动删文件
    """
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()

def write_one_galaxy(galaxy_name, M_b, eta, r0, r1, alpha, beta, R2):
    """写入一行星系数据"""
    data = {
        "星系名称": galaxy_name,
        "总重子质量(M⊙)": M_b,
        "η((km/s)²)": eta,
        "r0(kpc)": r0,
        "r1(kpc)": r1,
        "alpha": alpha,
        "beta": beta,
        "拟合优度R²": R2
    }
    with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow(data)

# ====================== 【你的原始数据】直接写入 ======================
# 这里自动把你所有星系数据写进去
def write_all_sample_data():
    samples = [
        ["D564-8",7.71e+07,3.28e+03,10.464,10.5,1.2,0.2,0.938],
        ["D631-7",6.59e+08,4.11e+04,50.826,50.8,1.2,0.2,0.884],
        ["DDO064",5.46e+08,5.91e+03,4.906,4.9,1.2,0.2,0.935],
        ["DDO154",3.91e+08,4.59e+03,4.264,4.3,1.2,0.2,0.886],
        ["DDO161",2.98e+09,2.10e+04,41.181,41.2,1.2,0.2,0.959],
        ["DDO168",7.52e+08,5.87e+03,4.055,4.1,1.2,0.2,0.807],
        ["ESO079-G014",6.62e+10,3.94e+04,18.868,18.9,1.2,0.2,0.944],
        ["ESO116-G012",7.53e+09,2.74e+04,11.898,11.9,1.2,0.2,0.955],
        ["ESO444-G084",2.91e+08,8.70e+03,3.218,3.2,1.2,0.2,0.982],
        ["F563-1",8.11e+09,2.15e+04,9.064,9.1,1.2,0.2,0.888],
        ["F563-V2",7.28e+09,1.99e+04,2.567,2.6,1.2,0.2,0.867],
        ["F565-V2",2.22e+09,2.25e+04,16.355,16.4,1.2,0.2,0.932],
        ["F568-V1",9.82e+09,1.89e+04,2.445,2.4,1.2,0.2,0.838],
        ["F571-V1",4.85e+09,1.32e+04,10.543,10.5,1.2,0.2,0.909],
        ["F574-1",1.00e+10,1.26e+04,4.224,4.2,1.2,0.2,0.923],
        ["F583-1",7.02e+09,1.23e+04,7.458,7.5,1.2,0.2,0.905],
        ["NGC0055",1.08e+10,9.59e+03,8.561,8.6,1.2,0.2,0.868],
        ["NGC0247",1.21e+10,4.85e+04,47.876,47.9,1.2,0.2,0.962],
        ["NGC0300",4.69e+09,2.31e+04,16.278,16.3,1.2,0.2,0.956],
        ["NGC1003",1.68e+10,3.30e+04,36.281,36.3,1.2,0.2,0.861],
        ["NGC1705",8.13e+08,8.12e+03,1.311,1.3,1.2,0.2,0.889],
        ["NGC2366",1.22e+09,3.16e+03,1.792,1.8,1.2,0.2,0.780],
        ["NGC2403",1.80e+10,5.96e+04,37.487,37.5,1.2,0.2,0.898],
        ["NGC3109",8.04e+08,3.32e+04,28.856,28.9,1.2,0.2,0.971],
        ["NGC3198",6.24e+10,4.70e+04,46.291,46.3,1.2,0.2,0.870],
        ["NGC3741",3.17e+08,8.07e+03,9.778,9.8,1.2,0.2,0.985],
        ["NGC6015",4.31e+10,7.20e+04,52.982,53.1,1.2,0.2,0.914],
        ["UGC00128",2.79e+10,1.68e+04,6.713,597.9,1.2,0.2,0.958],
        ["UGC00191",5.00e+09,8.82e+03,3.652,3.7,1.2,0.2,0.931],
        ["UGC00731",3.66e+09,7.60e+03,3.206,3.2,1.2,0.2,0.975],
        ["UGC00891",1.23e+09,2.47e+04,29.896,29.9,1.2,0.2,0.928],
        ["UGC01230",2.16e+10,1.45e+04,2.738,2.7,1.2,0.2,0.773],
        ["UGC01281",8.71e+08,2.27e+04,22.287,22.3,1.2,0.2,0.938],
        ["UGC02487",5.47e+11,1.43e+05,25.595,25.6,1.2,0.2,0.856],
        ["UGC04325",3.80e+09,9.72e+03,1.134,1.1,1.2,0.2,0.883],
        ["UGC04499",4.07e+09,1.01e+04,9.397,9.4,1.2,0.2,0.919],
        ["UGC05005",1.46e+10,3.06e+04,46.711,46.7,1.2,0.2,0.963],
        ["UGC05716",2.84e+09,8.65e+03,4.873,4.9,1.2,0.2,0.975],
        ["UGC05750",1.10e+10,1.02e+04,15.407,15.4,1.2,0.2,0.933],
        ["UGC05918",5.52e+08,3.33e+03,3.351,3.4,1.2,0.2,0.985],
        ["UGC05986",6.85e+09,1.74e+04,3.559,3.6,1.2,0.2,0.833],
        ["UGC05999",1.25e+10,1.53e+04,10.341,10.3,1.2,0.2,0.781],
        ["UGC06399",4.23e+09,1.59e+04,9.631,9.6,1.2,0.2,0.961],
        ["UGC06446",3.71e+09,9.61e+03,2.509,2.5,1.2,0.2,0.946],
        ["UGC06667",2.14e+09,1.33e+04,4.385,4.4,1.2,0.2,0.920],
        ["UGC06930",1.65e+10,3.69e+04,18.029,0.4,1.2,0.2,0.932],
        ["UGC06983",1.17e+10,1.56e+04,4.397,4.4,1.2,0.2,0.782],
        ["UGC07125",8.13e+09,4.21e+03,8.412,8.4,1.2,0.2,0.895],
        ["UGC07151",3.95e+09,6.70e+03,4.903,4.9,1.2,0.2,0.959],
        ["UGC07261",3.29e+09,1.56e+04,13.594,13.6,1.2,0.2,0.835],
        ["UGC07524",6.62e+09,8.05e+03,4.467,4.5,1.2,0.2,0.938],
        ["UGC07603",6.98e+08,7.59e+03,2.987,3.0,1.2,0.2,0.881],
        ["UGC07608",9.40e+08,2.23e+04,14.187,14.2,1.2,0.2,0.955],
        ["UGC07690",1.41e+09,3.97e+03,3.048,3.0,1.2,0.2,0.765],
        ["UGC08286",2.70e+09,1.17e+04,4.221,4.2,1.2,0.2,0.958],
        ["UGC08490",2.24e+09,9.17e+03,1.965,2.0,1.2,0.2,0.949],
        ["UGC08550",9.07e+08,6.03e+03,3.582,3.6,1.2,0.2,0.979],
        ["UGC10310",3.98e+09,5.45e+03,1.893,1.9,1.2,0.2,0.881],
        ["UGC12632",4.22e+09,7.04e+03,3.885,3.9,1.2,0.2,0.956],
        ["UGCA281",9.48e+07,4.57e+03,5.419,5.4,1.2,0.2,0.994],
        ["UGCA442",5.79e+08,7.62e+03,6.057,6.1,1.2,0.2,0.962],
    ]
    for row in samples:
        write_one_galaxy(*row)

# ====================== 【自动流程】清空 → 写入 → 画图 ======================
if __name__ == "__main__":
    print("🔄 正在自动清空旧CSV...")
    auto_clear_and_init_csv()

    print("🔄 正在自动写入所有星系数据...")
    write_all_sample_data()

    print("🔄 正在读取数据并拟合...")
    # --------------- 下面是你原本的画图代码，完全不变 ---------------
    def load_valid_data(csv_path):
        M_b_list = []
        eta_list = []
        R2_list = []
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    M_b = float(row["总重子质量(M⊙)"])
                    eta = float(row["η((km/s)²)"])
                    R2 = float(row["拟合优度R²"])
                    if R2 > 0.85 and 5e7 < M_b < 2e11:
                        M_b_list.append(M_b)
                        eta_list.append(eta)
                        R2_list.append(R2)
                except:
                    continue
        if len(M_b_list) < 3:
            print("❌ 有效样本不足，无法拟合")
            exit()
        return np.array(M_b_list), np.array(eta_list), np.array(R2_list)

    M_b, eta, weights = load_valid_data(CSV_FILE)

    # 拟合标度关系
    log_M = np.log10(M_b)
    log_eta = np.log10(eta)
    def linear_fit(x, k, b):
        return k * x + b
    popt, pcov = curve_fit(linear_fit, log_M, log_eta, sigma=1/weights)
    k_scale, b_scale = popt
    y_pred = linear_fit(log_M, k_scale, b_scale)
    ss_res = np.sum((log_eta - y_pred)**2)
    ss_tot = np.sum((log_eta - np.mean(log_eta))**2)
    scale_R2 = 1 - (ss_res / ss_tot)

    print(f"\n🔍 普适标度关系：η ∝ M_b^{k_scale:.2f}")
    print(f"📊 拟合优度R² = {scale_R2:.3f}")

    # 绘图
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['mathtext.fontset'] = 'dejavusans'

    plt.figure(figsize=(10, 8), dpi=120)
    plt.scatter(M_b, eta, s=60, color='#0066ff', label=f'高质量星系 (n={len(M_b)})', alpha=0.8)
    x_fit = np.logspace(np.log10(min(M_b)), np.log10(max(M_b)), 100)
    y_fit = 10**b_scale * x_fit**k_scale
    plt.plot(x_fit, y_fit, color='#ff2222', linewidth=2.5, label=f'η∝M_b^{k_scale:.2f}')
    plt.xscale('log')
    plt.yscale('log')
    plt.title(f"η与重子质量的普适标度关系 (R²={scale_R2:.3f})", fontsize=13, fontweight='bold')
    plt.xlabel("重子总质量 (M⊙)", fontsize=11)
    plt.ylabel("η ((km/s)$^2$)", fontsize=11)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig("优化后_普适标度关系.png", dpi=150, bbox_inches='tight')
    plt.show()

    print("\n✅ 全部完成！图像已保存！")