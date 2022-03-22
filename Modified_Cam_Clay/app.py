from Modified_Cam_Clay import *
import streamlit as st
from PIL import Image
import base64
import textwrap
import pandas as pd

def render_svg(svg_file,caption,width=576):
    with open(svg_file, "r") as f:
        lines = f.readlines()
        svg = "".join(lines)
        b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
        html = r'<div align="center"><img src="data:image/svg+xml;base64,%s" width=%s/><figcaption>%s</figcaption></div>' % (b64,str(width),caption)
        st.write(html, unsafe_allow_html=True)

st.set_page_config(initial_sidebar_state="expanded",menu_items={
         'About': """This is a web application to better understand the modified cam clay constitutive model.
         
Developed by:

Humberto Rojas Huaroto, humberto.rojas.h@uni.pe

[Linkedin](https://www.linkedin.com/in/humberto-rojas-huaroto-63908321a/)

Miguel Bernilla Lucero, mbernillal@uni.pe

[Linkedin](https://www.linkedin.com/in/miguel-angel-bernilla-lucero-6b745621a/)
         """
     })
st.title('Modified Cam Clay Constitutive Model')
st.markdown("#### Summary")
st.write('''In this report, the theoretical and practical analysis of the Modified Cam Clay Constitutive Model is carried out, one of 
which introduces us to the critical state theory to characterize a specific soil. First, it will be carried out
conceptual development of the subject to later take it to a practical application case and understand the operation of this modeling.''')
st.markdown("#### 1. Introduction")
st.write('''The study of constitutive models has had a great evolution in academic circles, but its application practice in design has been limited, mainly due to its low diffusion and the need to use a greater number of parameters than those required in traditional methodologies. On the other hand, it has come popularizing the use of computer applications specialized in geotechnics, which include within their options, the use of models based on the critical state theory. One of these models is called Modified Cam-Clay (CCM). The CCM model (Roscoe and Burland, 1968), is relatively easy to use and its Parameters can be found by conventional laboratory tests. However, it is not always adjusted to the real behavior of the materials.''')
st.markdown("#### 2. Theoretical development of the constitutive model")
st.write('''The Modified Cam Clay constitutive model is a model used mainly to represent soil types
clayey. This model was known in four properties: Elastic Properties, Yield Surface, Plastic Potential, and the
hardening law.''')
st.write('''In this model, it is assumed that the volume elastic strains are directly related to a change
in the stress $p'$ according to the expression:''')
st.latex(r"\begin{equation} \partial\varepsilon_{p}^{e}=\tfrac{k}{vp'}*\partial p' \end{equation}")
st.write('''This implies a linear relationship between the value of the specific volume $v$ and the logarithm of the stress $p'$ for a case
loading and unloading of the soil, this linear relationship is shown in Figure 1. These values are found from a test
of consolidation.''')
render_svg("img/fig1_mcc.svg","Figure 1. Graph v – ln(p')")
st.write('''The linear relationship between the logarithmic of the preconsolidation pressure and the specific volume is shown below''')
st.latex(r"\begin{equation} v=N-\lambda ln(p'_0) \end{equation}")
st.write('''Likewise, it is assumed that a change in the deviating stress q generates a shear elastic deformation of the form:''')
st.latex(r"\begin{equation} \partial \varepsilon_{q}^{e}=\frac{\partial q}{3G} \end{equation}")
st.write('''In the $p'-q$ plane for the Cam Clay model (Figure 2) we can observe the critical state line LEC, which has
as slope a value of M, in the same $p'-q$ plane, the yield surface can be represented as a curve
ellipsoidal, whose main characteristic is that the upper point is intersected by the critical state line
and that its size depends on the preconsolidation pressure $p'_0$, the equation of the ellipse is the following:
''')
st.latex(r"\begin{equation} \frac{p'}{p'_0}=\frac{M^{2}}{M^{2}+\frac{q^{2}}{p'^{2}}} \end{equation}")
st.write("Where a value of $n$ is defined as follows:")
st.latex(r"\begin{equation} n=\frac{q}{p'} \end{equation}")
st.write("Subtituting equation (5) in equation (4):")
st.latex(r"\begin{equation} \frac{p'}{p'_0}=\frac{M^{2}}{M^{2}+n^{2}} \end{equation}")
st.write("Rewriting Equation (6) we have the following yield surface expression:")
st.latex(r"\begin{equation} f=q^{2}-M^{2}\left [ p'(p'_0-p') \right ]=0 \end{equation}")

st.sidebar.markdown("### Yield Surface Parameters")
M = st.sidebar.number_input('Pendient of Critical State Line', min_value=0.00, max_value=2.00, value=1.00, step=0.01)
pc = st.sidebar.number_input('Preconsolidation Stress', min_value=100, max_value=1000, value=500, step=1)
fig = yield_surface(M,pc,30,80)
st.plotly_chart(fig)

st.write('''The values where the value of q is maximum, for the different yield surfaces, belong to the curve of
critical condition (CSL) (Figure 2).''')
render_svg("img/fig2_mcc.svg","Figure 2. Yield Surface of the Modified Cam Clay Model.")
st.write('''The soil is assumed to obey a normalized condition, so the plastic potential equation is practically the same
same as the yield surface in the $p'-q$ plane:''')
st.latex(r"\begin{equation} g=f=q^{2}-M^{2}\left [ p'(p'_0-p') \right ]=0 \end{equation}")
st.write('''When there is a stress that causes the creep equation to be exceeded, plastic deformations are generated, according to
generalized plastic stress theory, the plastic strains are found according to equations (9) and (10).''')
render_svg("img/fig3_mcc.svg","Figure 3. Yield surface and plastic potential for Ottawa dense sand.")
st.latex(r"\begin{equation} \partial \varepsilon _{p}^{p}=x*\frac{\partial g}{\partial p'} \end{equation}")
st.latex(r"\begin{equation} \partial \varepsilon _{q}^{p}=x*\frac{\partial g}{\partial q} \end{equation}")
st.write('''Where the value of $x$ is a scalar whose value will depend on the behavior of the soils. It is seen that a change in the
value of $p'_0$ ⁡generates a change in the plastic surface and also a change in a plastic volumetric strain and
plastic shear strain as shown in the following equation:''')
st.latex(r"\begin{equation} \partial p'_0=\frac{\partial p'_0}{\partial \varepsilon _{p}^{p}}*\partial \varepsilon _{p}^{p}+\frac{\partial p'_0}{\partial \varepsilon _{q}^{p}}*\partial \varepsilon _{q}^{p} \end{equation}")
st.write('''According to the aforementioned theory, the value of the scalar $x$ can be represented as follows:''')
st.latex(r"\begin{equation} x=-\frac{\left ( \frac{\partial f}{\partial p'}*\partial p'+\frac{\partial f}{\partial q}*\partial q\right )}{\frac{\partial f}{\partial p'_0}*\left ( \frac{\partial p'_0}{\partial \varepsilon _{p}^{p}}*\frac{\partial g}{\partial p'}+\frac{\partial p'_0}{\partial \varepsilon _{q}^{p}}*\frac{\partial g}{\partial q}\right )} \end{equation}")
st.write('''Substituting the value of x in equations (9) and (10) we have equation (16)''')
st.latex(r"""\begin{equation} \begin{bmatrix}\partial \varepsilon _{p}^{p}\\ \partial \varepsilon _{q}^{p}\end{bmatrix}=\frac{-1}{\frac{\partial f}{\partial p'_0}*\left ( \frac{\partial p'_0}{\partial \varepsilon _{p}^{p}}*\frac{\partial g}{\partial p'}+\frac{\partial p'_0}{\partial \varepsilon _{q}^{p}}*\frac{\partial g}{\partial q}\right )}\begin{bmatrix}
\frac{\partial f}{\partial p'}*\frac{\partial g}{\partial p'} & \frac{\partial f}{\partial q}*\frac{\partial g}{\partial p'} \\ 
\frac{\partial f}{\partial p'}*\frac{\partial g}{\partial q} & \frac{\partial f}{\partial q}*\frac{\partial g}{\partial q}\end{bmatrix}\begin{bmatrix}\partial p'\\ \partial q\end{bmatrix} \end{equation}""")
st.write('''In the case of the Cam-Clay model, we have the following relationship between the plastic strains:''')
st.latex(r"\begin{equation} \frac{\partial \varepsilon _{p}^{p}}{\partial \varepsilon _{q}^{p}}=\frac{x*\frac{\partial g}{\partial p'}}{x*\frac{\partial g}{\partial q}}=\frac{\frac{\partial g}{\partial p'}}{\frac{\partial g}{\partial q}}=\frac{M^{2}\left ( 2p'-p'_0 \right )}{2q}=\frac{M^{2}-n^{2}}{2n} \end{equation}")
st.write('''The variation of the plastic volumetric stresses according to the plastic theory is as follows:''')
st.latex(r"\begin{equation} \partial \varepsilon _{p}^{p}=\left [ \frac{\lambda -k}{v} \right ]*\frac{\partial p'_0}{p'_0} \end{equation}")
st.write('''Finding the elements of equation (11):''')
st.latex(r"\begin{equation} \frac{\partial p'_0}{\partial \varepsilon _{p}^{p}}=\frac{v*p'_0}{\lambda -k} \end{equation}")
st.latex(r"\begin{equation} \frac{\partial p'_0}{\partial \varepsilon _{q}^{p}}=0 \end{equation}")
st.write('''These equations must be substituted into the above equations to find the formulation of the equation elastoplastic.''')
st.markdown("#### 3. Formulation of the elasto-plastic equation")
st.write('''Combining equations (1) and (3), we have the following elastoplastic equations:''')
st.latex(r"\begin{equation} \begin{bmatrix} \partial \varepsilon _{p}^{e}\\\partial \varepsilon _{q}^{e} \end{bmatrix}=\begin{bmatrix} \frac{k}{vp'}& 0\\ 0 & \frac{1}{3G}\end{bmatrix}\begin{bmatrix}\partial p' \\ \partial q\end{bmatrix} \end{equation}")
st.write('''For the case of plastic deformations, equation (16) is modified''')
st.latex(r"\begin{equation} \begin{bmatrix} \partial \varepsilon _{p}^{p}\\\partial \varepsilon _{q}^{p}\end{bmatrix}=\begin{bmatrix} M^{2}-n^{2}& 2n\\ 2n & \frac{4n^{2}}{M^{2}-n^{2}}\end{bmatrix}\begin{bmatrix}\partial p' \\ \partial q\end{bmatrix} \end{equation}")
st.write('''Equation (18) is used for elastic deformations, while equation (19) is used when the soil enters into
the plastic range. Both general equations are necessary and relevant to find the deformations of the soil before
a change in the stresses, evaluating whether they are in the elastic or plastic range.''')
render_svg("img/fig4_mcc.svg","Figure 4. Cases in the Modified Cam Clay Model.")
st.write('''Employing the creep law, we can then see and predict the behavior of the soil, in case a, when
there is a change of stress from point A to point B, in this case, the initial stress is in the
yield surface, so that, as the stresses increase, it enters a plastic range, increasing the pressure of
preconsolidation and therefore modifying the yield law. In case of b, the initial stress state A is not found.
on the yield surface, which is why, when there is a change in the stress that does not reach the value of the surface
of yield, there are no plastic deformations and the value of the yield surface is not modified.''')
st.markdown("#### Case of an undrained triaxial test")
st.write(r'''In the present work, it will be evaluated in the case of an undrained triaxial test due to the data we have.
In an undrained case, since there is no water leakage, there is no volumetric change in the soil sample, so
the value of $\partial \varepsilon^{p}$ is 0, in other words, the sum of $\partial \varepsilon _{p}^{e}$ and $\partial \varepsilon _{p}^{p}$ equals zero.''')
st.latex(r"\begin{equation} \partial \varepsilon _{p}^{e}+\partial \varepsilon _{p}^{p}=0 \end{equation}")
st.write('''Substituting the values according to equations (1) and (15)''')
st.latex(r"\begin{equation} \frac{k}{vp'}*\partial p'=-\left [ \frac{\lambda -k}{v} \right ]*\frac{\partial p'_0}{p'_0} \end{equation}")
st.write('''Combining equation (21) with the creep equation, we get:''')
st.latex(r"\begin{equation} -\frac{\partial p'}{p'}=\left [ \frac{\lambda -k}{\lambda} \right ]*\frac{2n}{M^{2}+n^{2}}*\partial n \end{equation}")
st.write('''Integrating equation (22) with an initial p' for an initial value of n, we get:''')
st.latex(r"\begin{equation} \frac{p'_i}{p'}=\left ( \frac{M^{2}+n^{2}}{M^{2}+n_{i}^{2}} \right )^{\frac{\lambda -k}{\lambda }} \end{equation}")
st.write(r'''In the same way that in the general case there are 2 cases of analysis, which at the initial point of analysis is within
the yield surface and if it is on the yield surface. In the case that it is inside the surface,
there is a possibility of plastic deformations, so $\partial \varepsilon _{p}^{p} = 0$ and according to equation (20), $\partial \varepsilon _{p}^{e}$ would also be 0, for
which means that there is no elastic deformation, which implies that the effective stresses remain constant. In conclusion,
when there is an over-consolidated sample and an undrained test is performed, there is no variation in stress $p'$, only
of the value of $q$, this until it reaches the yield surface, hence the soil has a plastic behavior, such as
is shown in figure 5.''')
render_svg("img/fig5_mcc.svg","Figure 5. Case of an overconsolidated sample.")
st.write('''In the case of our model, depending on whether our initial point of analysis is to the right or the
left of the critical state line $(n=M)$, in the case, it is on the right, the soil will present a behavior
of hardening until it intersects the CSL, in the case it is on the right side, it will present a
softening behavior until approaching the CSL.''')
render_svg("img/fig6_mcc.svg","Figure 6. Case of soil softening and hardening.")
st.write('''An increase in the effective stress $p'$, generates a change in the effective stress $p$, relating it to the
$u$ value, also known as the pore pressure.''')
st.latex(r"\begin{equation} \partial u=\partial p-\partial p' \end{equation}")
st.write('''In an undrained triaxial test, if following the bases of the p-q graph according to Cambridge, it is defined:''')
st.latex(r"\begin{equation} \partial q= 3\partial p \end{equation}")
st.write('''With initial conditions of the form $p=p'_0$, $q= 0$, obtained upon integration is''')
st.latex(r"\begin{equation} p=\frac{q}{3}+p'_0 \end{equation}")
st.write('''Integrating equation (24) and substituting equation (26), we obtain:''')
st.latex(r"\begin{equation} u=\frac{q}{3}+p'_0-p' \end{equation}")
st.write('''For a better understanding of the model, examples of the behavior in the $p'-q$ plane are shown, the interaction of
the yield surface and the shear strain value according to the stress variation $q$ in the case of a soil
normally consolidated and overconsolidated respectively:''')
render_svg("img/fig7_mcc.svg","Figure 7. Conventional undrained triaxial test in normal soil compression: (a) Stress plane p'-q; (b) Stress-strain graph.")
render_svg("img/fig8_mcc.svg","Figure 8. Conventional undrained triaxial test in slightly overconsolidated soils: (a) Stress plane p'-q; (b) Stress-strain graph.")
render_svg("img/fig9_mcc.svg","Figure 9. Conventional undrained triaxial test in strongly overconsolidated soils: (a) Stress plane p'-q; (b) Stress-strain graph.")
st.write('''To find the strains in the case of the undrained triaxial test, we must apply the general strains
expressed in equations (18) and (19) but considering the boundary conditions of the CU triaxial test, having
as a result the following equations:''')
st.latex(r"\begin{equation} \partial \varepsilon _{p}^{p}=-\partial \varepsilon _{p}^{e} \end{equation}")
st.latex(r"\begin{equation} \partial \varepsilon _{q}^{p}=\frac{2n*\partial \varepsilon _{p}^{p}}{M^{2}-n^{2}} \end{equation}")
st.markdown("#### 4. Application")
st.write('''For the case of analysis, the laboratory data found in the paper “Application of the model
modified cam-clay in reconstituted clays from the Bogotá savannah”, where the triaxial and
consolidation tests to find the necessary parameters.

Triaxial tests help us determine the value of $M$, $G$ and $p'_i$, which are the slope of the line of
critical state, the shear modulus of the soil, and the initial stress applied.

Consolidation tests are used to find $λ$, $k$, which is the slope of the specific volume plot.
vs $log(p')$, as well as the value of $p'_0$ or pre-consolidation state, as well as the value of $N$, which is the point
maximum of the graph.

The test results are as follows in the sidebar:

Based on these parameters, we will find the displacements, stresses, pore pressure, and graphs of these results.''')

st.sidebar.markdown("### Parameters of Triaxial Test")
st.sidebar.write("Format data: [ $\lambda $, $k$, $M$]")
parameters = st.sidebar.text_input("Parameters","[0.168, 0.071, 0.96]")

parameters = eval(parameters)
λ, k, M = parameters
number_test=st.sidebar.number_input("Number of tests",min_value=1,max_value=20,value=3, step=1)

data =[]
st.sidebar.write("Format data: [ $p'_0$,  $p'$,  $G$,  $N$ ] (kPa)")
if number_test==3:
    sp1 = st.sidebar.text_input("Specimen number "+str(1),"[490, 449, 17711, 1.85]")
    sp2 = st.sidebar.text_input("Specimen number "+str(2),"[556, 556, 25300, 1.86]")
    sp3 = st.sidebar.text_input("Specimen number "+str(3),"[623, 623, 27803, 1.84]")
    data.append(eval(sp1))
    data.append(eval(sp2))
    data.append(eval(sp3))
else:
    for i in range(int(number_test)):
        sp4 = st.sidebar.text_input("Specimen number "+str(i+1))
        try:
            if type(eval(sp4)) == list:
                data.append(eval(sp4))
        except:pass
Points = st.sidebar.number_input("Number of points in curve",min_value=1,max_value=100,value=20, step=1)
Condition = st.sidebar.selectbox('Condicion of Triaxial Test',("Undrained",))

if len(data)==0:
         pass
else:
         results = cam_clay_modified(M, λ, k, data, int(Points), Condition)
         e_max=max([dff.loc[dff.index[-1], "ε"] for dff in results])*1.2
         results_f=[]
         for df in results:
            data2 =pd.DataFrame({"p'":[df.loc[df.index[-1], "p'"]], "q":[df.loc[df.index[-1], "q"]], "µ":[df.loc[df.index[-1], "µ"]], "ε":[e_max]})
            df3 = df.append(data2, ignore_index = True)
            results_f.append(df3)

         for i,datas in enumerate(results_f):
             st.write("Specimen number "+str(i+1)+" (p' = "+str(datas["p'"][0])+")")
             st.dataframe(datas)
         file=""""""
         for i,df in enumerate(results_f):
             file = file+"Specimen number "+str(i+1)+" (p' = "+str(df["p'"][0])+")"+"\n\n"
             string=df.to_string()
             file = file +string
             file = file + "\n\n"
         st.download_button(
     label="Download data as txt",
     data=file,
     file_name='Data.txt')

         fig2 = p_vs_q(M,results_f)
         st.plotly_chart(fig2)

         fig3 = q_vs_ε(M,results_f)
         st.plotly_chart(fig3)
 
st.markdown("### References")
st.write("""8, P.V. (s.f.). *Manual of material models*.

BORJA, R.I., & Lee, S.R. (1990). Cam Clay Plasticity, Part I: Implicit Integration of Constitutive Elasto-Plastic
Relations. *COMPUTER METHODS IN MECHANICS AND APPLIED ENGINEERING 78*, 49-72.

Camacho, J., & Reyes, O. (s. f.). Application of the modified cam-clay model in reconstituted clays from the savannah
from Bogota. *Construction Engineering Magazine*, 20.

Wood, D. M. (1990). *Soil behavior and soil mechanics in critical condition*. Cambridge: Cambridge University Press.

https://soilmodels.com/soilanim/
""")
