import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.optimize import curve_fit
from sklearn.utils import resample

# ====================== 读取清洗后的数据 ======================
file = "清洗后_172有效样本.csv"
M = []
E = []
w = []
rows = []
with open(file, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    for row in reader:
        try:
            mb = float(row["总重子质量(M⊙)"])
            et = float(row["η((km/s)²)"])
            r2 = float(row["拟合优度R²"])
            if r2 > 0:  # 只留R²正的
                M.append(mb)
                E.append(et)
                w.append(r2)
                rows.append(row)
        except:
            continue

M = np.array(M)
E = np.array(E)
w = np.array(w)
print(f"✅ 初始有效样本：{len(M)}个")

# 对数变换
logM = np.log10(M)
logE = np.log10(E)

# ====================== 第一步：3σ离群点剔除 ======================
def linear(x, k, b):
    return k * x + b

# 初步拟合
popt, _ = curve_fit(linear, logM, logE, sigma=1/(w+1e-6))
y_pred = linear(logM, *popt)
res = np.abs(logE - y_pred)
# 3σ剔除
mask = res < 3 * np.std(res)
M_c = M[mask]
E_c = E[mask]
w_c = w[mask]
logM_c = logM[mask]
logE_c = logE[mask]
rows_c = [rows[i] for i in range(len(rows)) if mask[i]]
print(f"✅ 3σ剔除后样本：{len(M_c)}个")

# ====================== 第二步：加权最小二乘拟合 ======================
popt, pcov = curve_fit(linear, logM_c, logE_c, sigma=1/(w_c+1e-6))
k, b = popt
dk, db = np.sqrt(np.diag(pcov))

# R²
y_pred_c = linear(logM_c, k, b)
r2 = 1 - np.sum((logE_c - y_pred_c)**2) / np.sum((logE_c - np.mean(logE_c))**2)

# ====================== 第三步：Bootstrap误差估计 ======================
n_boot = 1000
k_boot = []
for _ in range(n_boot):
    idx = resample(np.arange(len(logM_c)))
    xb, yb, wb = logM_c[idx], logE_c[idx], w_c[idx]
    popt_b, _ = curve_fit(linear, xb, yb, sigma=1/(wb+1e-6))
    k_boot.append(popt_b[0])
k_boot = np.array(k_boot)
k_err = np.std(k_boot)

# ====================== 输出结果 ======================
print("="*60)
print("🎯 终极完善后的最终结果")
print("="*60)
print(f"标度指数：k = {k:.4f} ± {dk:.4f} (Bootstrap误差: ±{k_err:.4f})")
print(f"归一化常数：C = {10**b:.4f}")
print(f"拟合优度 R² = {r2:.4f}")
print(f"最终公式：η = {10**b:.4f} · M_b^({k:.3f}±{k_err:.3f})")
print("="*60)

# ====================== 保存最终的干净数据 ======================
new_file = "终极清洗_最终有效样本.csv"
with open(new_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows_c)
print(f"\n✅ 已保存最终干净CSV：{new_file}")

# ====================== 绘图 ======================
plt.rcParams.update({
    "font.sans-serif": ["SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.dpi": 150
})
plt.figure(figsize=(10,8))
plt.scatter(M_c, E_c, s=50, c="#0066ff", alpha=0.8, label=f"最终样本 n={len(M_c)}")
x_fit = np.logspace(np.log10(min(M_c)), np.log10(max(M_c)), 100)
y_fit = 10**b * x_fit**k
plt.plot(x_fit, y_fit, c="#ff2222", linewidth=3, label=fr"$\eta \propto M_b^{{{k:.3f}\pm{k_err:.3f}}}$")
plt.xscale("log")
plt.yscale("log")
plt.xlabel(r"总重子质量 $M_b\ (M_\odot)$", fontsize=12)
plt.ylabel(r"$\eta\ (\mathrm{(km/s)^2})$", fontsize=12)
plt.title(fr"终极完善版 $\eta$–$M_b$ 标度关系 | $R^2={r2:.4f}$", fontweight="bold", fontsize=14)
plt.grid(alpha=0.3, ls="--")
plt.legend()
plt.tight_layout()
plt.savefig("终极完善版_标度关系.png", dpi=300)
plt.show()

# ====================== 残差分析 ======================
residuals = logE_c - y_pred_c
plt.figure(figsize=(10,5))
plt.scatter(logM_c, residuals, s=30, c="#00aa00", alpha=0.7)
plt.axhline(0, color="red", linestyle="--")
plt.xlabel(r"$\log_{10} M_b$", fontsize=12)
plt.ylabel(r"残差 $\log_{10} \eta - 拟合值$", fontsize=12)
plt.title("残差分布", fontweight="bold")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("残差分析.png", dpi=300)
plt.show()

print("\n✅ 全部完成！这就是我们能做到的最精确的结果了！")