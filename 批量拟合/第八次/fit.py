import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from scipy.stats import theilslopes, pearsonr

CSV_FILE = "有效拟合星系结果.csv"

# ====================== 纯读取你的数据，不做任何修改 ======================
def load_your_data():
    M_b = []
    eta = []
    names = []
    with open(CSV_FILE, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                mb = float(row["总重子质量(M⊙)"])
                et = float(row["η((km/s)²)"])
                name = row["星系名称"]
                M_b.append(mb)
                eta.append(et)
                names.append(name)
            except:
                continue
    return np.array(M_b), np.array(eta), names

# ====================== 主运行 ======================
if __name__ == "__main__":
    M_b, eta, names = load_your_data()
    print(f"📊 你的原始样本数：{len(M_b)}")
    
    # 对数变换
    logM = np.log10(M_b)
    logE = np.log10(eta)
    
    # 计算相关系数
    corr, p = pearsonr(logM, logE)
    print(f"📊 原始相关系数：{corr:.4f}, p值：{p:.4f}")
    
    # Theil-Sen稳健拟合
    res = theilslopes(logE, logM)
    k, b, k_low, k_high = res
    dk = (k_high - k_low) / 2
    
    # R²
    y_pred = k * logM + b
    r2 = 1 - np.sum((logE - y_pred)**2) / np.sum((logE - np.mean(logE))**2)
    
    # 输出
    print("="*60)
    print("🎯 你的真实数据的结果（完全客观，无任何假设）")
    print("="*60)
    print(f"标度指数：k = {k:.4f} ± {dk:.4f}")
    print(f"拟合优度 R² = {r2:.4f}")
    print(f"标度关系：η ∝ M_b^({k:.3f}±{dk:.3f})")
    print("="*60)
    
    # 绘图
    plt.rcParams.update({
        "font.sans-serif": ["SimHei", "DejaVu Sans"],
        "axes.unicode_minus": False,
        "figure.dpi": 150
    })
    plt.figure(figsize=(10,8))
    
    plt.scatter(M_b, eta, s=60, c="#0066ff", alpha=0.8, label=f"你的样本 n={len(M_b)}")
    x_fit = np.logspace(np.log10(min(M_b)), np.log10(max(M_b)), 100)
    y_fit = 10**b * x_fit**k
    plt.plot(x_fit, y_fit, c="#ff2222", linewidth=3, label=fr"拟合线 $\eta \propto M_b^{{{k:.3f}\pm{dk:.3f}}}$")
    
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel(r"总重子质量 $M_b\ (M_\odot)$", fontsize=12)
    plt.ylabel(r"$\eta\ (\mathrm{(km/s)^2})$", fontsize=12)
    plt.title(fr"你的模型的 $\eta$–$M_b$ 标度关系 | $R^2={r2:.4f}$", fontweight="bold", fontsize=14)
    plt.grid(alpha=0.3, ls="--")
    plt.legend()
    plt.tight_layout()
    plt.savefig("你的真实数据_标度关系.png", dpi=300, bbox_inches="tight")
    plt.show()
    
    print("\n✅ 全部完成！这就是你数据的真实结果！")