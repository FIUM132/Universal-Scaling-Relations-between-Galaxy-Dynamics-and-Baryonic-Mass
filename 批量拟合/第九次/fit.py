import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.stats import theilslopes

# ====================== 读取172个的原始数据 ======================
file172 = "有效拟合星系结果_172.csv"
M = []
E = []
rows = []
with open(file172, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    for row in reader:
        try:
            mb = float(row["总重子质量(M⊙)"])
            et = float(row["η((km/s)²)"])
            # 只保留拟合成功的点
            if et > 100:
                M.append(mb)
                E.append(et)
                rows.append(row)
        except:
            continue

M = np.array(M)
E = np.array(E)
print(f"✅ 原始172个，清洗后剩余有效样本：{len(M)}个")

# ====================== 拟合 ======================
logM = np.log10(M)
logE = np.log10(E)
res = theilslopes(logE, logM)
k, b, k_low, k_high = res
dk = (k_high - k_low) / 2
y_pred = k * logM + b
r2 = 1 - np.sum((logE - y_pred)**2) / np.sum((logE - np.mean(logE))**2)

# 输出
print("="*60)
print("🎯 清洗后172样本的最终结果")
print("="*60)
print(f"标度指数：k = {k:.4f} ± {dk:.4f}")
print(f"拟合优度 R² = {r2:.4f}")
print(f"标度关系：η ∝ M_b^({k:.3f}±{dk:.3f})")
print("="*60)

# ====================== 保存新的CSV ======================
new_file = "清洗后_172有效样本.csv"
with open(new_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
print(f"\n✅ 已保存清洗后的CSV：{new_file}")

# ====================== 绘图 ======================
plt.rcParams.update({
    "font.sans-serif": ["SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.dpi": 150
})
plt.figure(figsize=(10,8))
plt.scatter(M, E, s=50, c="#0066ff", alpha=0.8, label=f"有效样本 n={len(M)}")
x_fit = np.logspace(np.log10(min(M)), np.log10(max(M)), 100)
y_fit = 10**b * x_fit**k
plt.plot(x_fit, y_fit, c="#ff2222", linewidth=3, label=fr"$\eta \propto M_b^{{{k:.3f}\pm{dk:.3f}}}$")
plt.xscale("log")
plt.yscale("log")
plt.xlabel(r"总重子质量 $M_b\ (M_\odot)$", fontsize=12)
plt.ylabel(r"$\eta\ (\mathrm{(km/s)^2})$", fontsize=12)
plt.title(fr"清洗后172样本的 $\eta$–$M_b$ 标度关系 | $R^2={r2:.4f}$", fontweight="bold", fontsize=14)
plt.grid(alpha=0.3, ls="--")
plt.legend()
plt.tight_layout()
plt.savefig("清洗后172样本_标度关系.png", dpi=300)
plt.show()

print("\n✅ 全部完成！你后续就用这个新的CSV来继续分析就可以了！")