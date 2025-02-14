# cell_segment_gui
segment by stardist (pytorch)  , GUI by pyqt
import casadi as ca

# 定义符号变量
x1 = ca.MX.sym('x1')
x2 = ca.MX.sym('x2')
x = ca.vertcat(x1, x2)
u = ca.MX.sym('u')

# 定义微分方程
ode = ca.vertcat((1 - x2**2) * x1 - x2 + u, x1)

# 创建函数
f = ca.Function('f', [x, u], [ode], ['x', 'u'], ['ode'])

# 设置积分器参数
t0 = 0
T = 10
N = 20
tf = T / N
intg_options = {
    'simplify': True,
    'number_of_finite_elements': 4
}

# 定义DAE（微分代数方程）
dae = {
    'x': x,
    'p': u,
    'ode': f(x, u)
}

# 创建积分器
intg = ca.integrator('intg', 'rk', dae, intg_options)

# 计算下一个状态
res = intg(x0=x, p=u)
x_next = res['xf']
F = ca.Function('F', [x, u], [x_next], ['x', 'u'], ['x_next'])

# 创建一个累积映射函数
sim = F.mapaccum(N)

# 打印形状
print(x.shape)
print(ode.shape)
