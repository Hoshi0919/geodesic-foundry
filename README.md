# Geodesic Foundry (测地工场)

> **Curved Spacetime Logistics & Penrose Ergosphere Accelerator**  
> 广义相对论时空测地线物流与黑洞能层反应器建造模拟器

---

## 概述 (Overview)

**Geodesic Foundry** 是一个彻底颠覆传统“传送带/机械臂/管道”自动化范式的开创性建造模拟器。

在弯曲时空中，**没有传送带，没有机械推力，物料粒子仅仅是自由落体的试验质量点（Test Particles）**。整个工场的流水线完全由广义相对论的几何曲率（Metric Curvature）编织而成。玩家通过布置微型史瓦西黑洞、自旋克尔黑洞、引力透镜与负质量奇异物质核，利用天体物理学动力学完成无接触的物料分选、裂解增能与超冷冻运输。

---

## 四大核心力学 (Core Relativistic Mechanics)

### 1. 测地引力透镜色散分选 (Gravitational Lensing & Relativistic Chute)
- 相对论偏转角对速度与能量具备色散依赖：
  $$\Delta \phi \approx \frac{2GM}{b v^2} \left(1 + \frac{v^2}{c^2}\right)$$
- 高能超相对论光子束（$v \to c, \Delta\phi \to \frac{4GM}{c^2 b}$）与低速经典重核束流（$\Delta\phi \to \frac{2GM}{v^2 b}$）掠过中央史瓦西质量井时，因偏转角度截然不同而自发分流至上下独立轨道接收靶位，实现零接触几何级物料色散分选。

### 2. 彭罗斯过程与黑洞自旋能提取 (Penrose Ergosphere Accelerator)
- 克尔旋转黑洞周围存在能层（Ergosphere，$r_+ < r \le r_E$），其内类时 Killing 矢量转变为类空，允许存在相对于无穷远观测者具有负能量的轨道态（$E < 0$）。
- 物料原坯以掠射角进入能层并发生潮汐裂解：
  $$E_{\text{esc}} = E_0 - E_{\text{absorbed}} > E_0$$
- 负能碎片坠落视界并减速黑洞自旋，正能超辐射脉冲以 140%+ 动能狂暴喷射而出，直接充入高能受体电池。

### 3. 引力时间膨胀低温井 (Gravitational Time Dilation Cryo-Well)
- 放射性同位素在平直时空中具有极短的本征半衰期（$\tau_{1/2}$），常规长距离运输将在半途自然衰变损耗。
- 通过引导物料切入强引力井的近视界稳定轨道，利用施瓦西时间膨胀因子：
  $$\frac{d\tau}{dt} = \sqrt{1 - \frac{2GM}{r c^2} - \frac{v^2}{c^2}}$$
  将物料本征时几乎冻结（$d\tau/dt \to 0.1 \sim 0.3$），使其在实验室参考系中存活时间拉长数倍，完好无损地跨越星际工场运达合成工位。

### 4. 1PN 后牛顿动力学与伦斯-蒂尔林效应 (1PN Geodesic & Frame Dragging)
- 数值内核采用 1PN（第一阶后牛顿修正）辛 Verlet 积分器，完整复现爱因斯坦广义相对论测地线进动、相对论速度加重与克尔黑洞自旋参考系拖拽力偶。

---

## 场景体验 (Scenarios)

1. **场景 1：引力透镜分选机 (`lensing`)**：光子束与重核天然按相对论偏转角无接触分流；
2. **场景 2：彭罗斯黑洞能层超辐射 (`penrose`)**：切入旋转能层提取黑洞自旋能，超能反冲；
3. **场景 3：时间膨胀低温井 (`dilation`)**：短命同位素借力引力深井冻结寿命安全运输；
4. **场景 4：自由时空沙盒 (`freeform`)**：可自由拖拽多奇点，实时观察弯曲度规与物流网自运转。

---

## 快速上手 (Quick Start)

### 本地运行与体验
无需安装任何复杂依赖，直接用现代浏览器打开 `index.html` 即可完整体验：
```bash
# 启动本地轻量 HTTP 服务预览
python3 -m http.server 8080 -d /hoshi/projects/geodesic-foundry
```

### Python 动力学仿真内核测试
```bash
cd /hoshi/projects/geodesic-foundry
pytest
```

---

## 许可证 (License)

MIT License © 2026 Hoshi
