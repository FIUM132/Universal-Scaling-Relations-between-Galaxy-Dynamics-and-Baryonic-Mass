import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import csv
import os

# 自动在当前文件夹里找csv文件
def find_csv_file():
    # 先在当前目录找
    for f in os.listdir('.'):
        if f.endswith(".csv") and "有效拟合" in f:
            return f
    # 再在子文件夹里找
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith(".csv") and "有效拟合" in f:
                return os.path.join(root, f)
    return None

# 自动查找文件
csv_file = find_csv_file()
if csv_file is None:
    print("❌ 错误：在SPARC文件夹里找不到有效拟合的csv文件！")
    print("💡 提示：请确保你的csv文件里包含'有效拟合'字样，或者手动指定文件路径")
    exit()

print(f"✅ 自动找到csv文件：{csv_file}")

# 修复中文+上标符号显示问题
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'dejavusans'

# 读取数据
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

M_b, eta, weights = load_valid_data(csv_file)

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

print(f"\n🖼️  标度关系图已保存至当前文件夹！")