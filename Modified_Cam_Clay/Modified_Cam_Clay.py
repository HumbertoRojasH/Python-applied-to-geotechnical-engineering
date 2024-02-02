from numpy import linspace, meshgrid, sin, pi, log, array, zeros
import plotly.graph_objects as go
import pandas as pd

def yield_surface(M,pc,theta,puntos):
  θ = linspace(-pi,pi,theta)
  p = linspace(0,pc,puntos)
  θ,p = meshgrid(θ,p)
  q=(M**2*p*(pc-p))**0.5
  x= p + 2/3*q*sin(θ-2*pi/3)
  y= p + 2/3*q*sin(θ)
  z= p + 2/3*q*sin(θ+2*pi/3)

  fig = go.Figure()
  fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.5,colorscale=[[0, "blue"], [1, "blue"]],showscale=False))
  fig.add_trace(go.Scatter3d(x=[0,pc*1.5],y=[0,pc*1.5],z=[0,pc*1.5],text=["","σ1=σ2=σ3"],mode ="lines+text"))
  fig.add_trace(go.Cone(x=[pc*1.5], y=[pc*1.5], z=[pc*1.5], u=[pc/10], v=[pc/10], w=[pc/10],showscale=False))
  fig.update_layout(
      showlegend=False,
      width=700,
      scene = dict(xaxis_title='σ1',
                  yaxis_title='σ2',
                  zaxis_title='σ3'),
      margin=dict(r=0, l=0, b=0, t=0))
  return fig

def deformation(N, M, λ, k, G, pc, Δp, p, Δq, n, e, test):
  v = N-λ*log(pc)

  # elastic deformation
  matrix_elastic = array([[ k/(v*p),    0    ],
                             [   0    , 1/(3*G) ]])
  [εe_p, εe_q] = matrix_elastic@array([Δp,Δq])

  # plastic deformation
  if test=="Drained":
    matrix_plastic = (λ-k)/(v*p*(M**2+n**2))*array([[ M**2-n**2,        2*n         ],
                                                       [    2*n   , 4*n**2/(M**2-n**2) ]])
    [εp_p, εp_q] = matrix_plastic@array([Δp,Δq])
  elif test=="Undrained":
    εp_p = -εe_p
    εp_q = (2*n*εp_p)/(M**2-n**2)
  
  ε = εe_p + εe_q + εp_p + εp_q
  e = e + ε
  return e

def cam_clay_undrained(M, λ, k, specimen, Points, Condition):
  [n, pc, p, q, u, e] = zeros((6,Points))
  pc[0] = specimen[0]
  p[0] = specimen[1]
  G = specimen[2]
  N = specimen[3]+λ*log(pc[0])
  EXP = (λ-k)/λ
  Type = ""

  #Overconsolidated
  if p[0]<pc[0]:
    pc[1]=pc[0]
    p[1]=p[0]
    q[1] = (M**2*(p[1]*(pc[1]-p[1])))**0.5
    n_inicial = q[1]/p[1]
    u[1] = q[1]/3+p[0]-p[1]
    if n_inicial<M: 
      Type = "Hardening"
      n[1:] = linspace(n_inicial, M-0.01, Points-1)
    else: 
      Type = "Softening"
      n[1:] = linspace(n_inicial, M+0.01, Points-1)

  #Normallyconsolidated
  else:
    n_inicial = 0.05
    p[1] = p[0]*((M**2)/(M**2+n_inicial**2))**EXP
    pc[1] = p[1]*(M**2+n_inicial**2)/( M**2)
    q[1] = n_inicial*p[1]
    u[1] = q[1]/3+p[0]-p[1]
    Type = "Hardening"
    n[1:] = linspace(n_inicial, M-0.01, Points-1)

  e[1] = deformation(N, M, λ, k, G, pc[1], 0, p[1], q[1], n[1], e[0], Condition)

  for i in range(2,Points):
    # invariants
    p[i] = p[i-1]*((M**2+n[i-1]**2)/(M**2+n[i]**2))**EXP
    pc[i] = p[i]*(M**2+n[i]**2)/( M**2)
    q[i] = n[i]*p[i]

    # pore pressure
    u[i] = q[i]/3+p[0]-p[i]

    # deformation
    Δp = p[i]-p[i-1]
    Δq = q[i]-q[i-1]
    e[i] = deformation(N, M, λ, k, G, pc[i], Δp, p[i], Δq, n[i], e[i-1], Condition)
  
  return p, q, u, e, Type

def cam_clay_modified(M, λ, k, Test, Points, Condition):
  results = []

  for specimen in Test:

    if Condition=="Undrained":
      p, q, u, e, Type = cam_clay_undrained(M, λ, k, specimen, Points, Condition)
    elif Condition=="Drained": pass

    data = {"p'":p, "q":q, "µ":u, "ε":e}
    df = pd.DataFrame(data)
    results.append(df)
  return results

def p_vs_q(M,results):
  fig = go.Figure()
  for df in results:
    fig.add_trace(go.Scatter(x=df["p'"], y=df["q"],mode='lines+markers', name="p' = "+str(df["p'"][0])+" kPa"))
    
  #if Type == "Hardening":
   # fig.add_trace(go.Scatter(x=[0,results[0]["p'"][-1]*1.5, y=[0,M*results[0]["p'"][-1]*1.5],mode='lines', name="Critical State Line (CSL)"))
  #else:
  dff = results[-1]
  fig.add_trace(go.Scatter(x=[0,dff.loc[dff.index[-1], "p'"]*1.2], y=[0,M*dff.loc[dff.index[-1], "p'"]*1.2],mode='lines', name="Critical State Line (CSL)"))
  fig.update_layout(title=dict(text="Mean Effective Stress vs Deviatoric Stress",x=0.5,xanchor='center', font=dict(size=24)),
                      legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),
                      xaxis_title="p' (kPa)",
                      yaxis_title="q (kPa)")
  return fig


def q_vs_ε(M,results):
  fig = go.Figure()
  for df in results:
    fig.add_trace(go.Scatter(x=df["ε"], y=df["q"],mode='lines+markers', name="p' = "+str(df["p'"][0])+" kPa"))
    
  fig.update_layout(title=dict(text="Deformation vs Deviatoric Stress",x=0.5,xanchor='center', font=dict(size=24)),
                    legend=dict(yanchor="bottom",y=0.01,xanchor="right",x=0.99),
                    xaxis_title="ε",
                    yaxis_title="q (kPa)")
  return fig
def u_vs_ε(M,results):
  fig = go.Figure()
  for df in results:
    fig.add_trace(go.Scatter(x=df["ε"], y=df["µ"],mode='lines+markers', name="p' = "+str(df["p'"][0])+" kPa"))
    
  fig.update_layout(title=dict(text="Deformation vs Excess Pore Pressure ",x=0.5,xanchor='center', font=dict(size=24)),
                    legend=dict(yanchor="bottom",y=0.01,xanchor="right",x=0.99),
                    xaxis_title="ε",
                    yaxis_title="u (kPa)")
  return fig
