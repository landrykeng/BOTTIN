import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

def show():
    if not st.session_state.get("authenticated", False):
        st.warning(":material/lock: Cette section est réservée aux utilisateurs enregistrés.")
        if st.button(":material/login: Se connecter"):
            st.session_state["page"] = "Connexion"; st.rerun()
        return

    st.title("Outils de calcul et de simulation")
    st.caption("Calculateurs interactifs mis à disposition des utilisateurs connectés.")

    tab1, tab2, tab3 = st.tabs([
        ":material/calculate: Calculateur de rendement",
        ":material/trending_up: Simulateur d'investissement",
        ":material/compare: Comparateur d'instruments",
    ])

    # ── Tab 1 : Calculateur de rendement ─────────────────────────────────────
    with tab1:
        st.markdown("### Calculateur de rendement obligataire")
        st.markdown("Saisissez les caractéristiques de l'instrument pour obtenir le rendement actuariel, la duration et la sensibilité.")

        col_i, col_r = st.columns([2, 2])

        with col_i:
            valeur_nominale = st.number_input("Valeur nominale (XAF)", value=1_000_000, step=100_000, format="%d")
            prix_achat = st.number_input("Prix d'achat (% du nominal)", value=98.5, min_value=50.0, max_value=120.0, step=0.1, format="%.2f")
            taux_facial = st.number_input("Taux facial / coupon (%)", value=6.5, min_value=0.0, max_value=20.0, step=0.1, format="%.2f")
            duree_annees = st.slider("Durée résiduelle (années)", 0, 15, 5)
            frequence = st.selectbox("Fréquence des coupons", ["Annuel","Semestriel"])

        with col_r:
            if duree_annees > 0:
                # Calcul actuariel simplifié
                freq = 1 if frequence == "Annuel" else 2
                coupon = valeur_nominale * (taux_facial / 100) / freq
                prix = valeur_nominale * (prix_achat / 100)
                n = duree_annees * freq

                # Newton-Raphson pour le taux actuariel
                def prix_bond(r):
                    return sum(coupon / (1 + r/freq)**t for t in range(1, n+1)) + valeur_nominale / (1 + r/freq)**n

                r = taux_facial / 100
                for _ in range(100):
                    f_r = prix_bond(r) - prix
                    r_eps = r + 1e-6
                    f_eps = prix_bond(r_eps) - prix
                    deriv = (f_eps - f_r) / 1e-6
                    if abs(deriv) < 1e-12: break
                    r -= f_r / deriv

                # Duration de Macaulay
                flux_actualises = [(t/freq) * (coupon / (1 + r/freq)**t) for t in range(1, n+1)]
                flux_actualises[-1] += duree_annees * (valeur_nominale / (1 + r/freq)**n)
                duration = sum(flux_actualises) / prix_bond(r)
                sensibilite = -duration / (1 + r/freq)

                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:1rem;">
                    <div class="metric-label">Rendement actuariel</div>
                    <div class="metric-value" style="color:#003366;">{r*100:.4f} %</div>
                </div>
                """, unsafe_allow_html=True)

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Duration</div><div class="metric-value" style="font-size:1.5rem;">{duration:.2f} ans</div></div>""", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Sensibilité</div><div class="metric-value" style="font-size:1.5rem;">{sensibilite:.3f}</div></div>""", unsafe_allow_html=True)
                with c3:
                    gain = (prix_bond(r) - prix) + coupon * duree_annees
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Gain total net</div><div class="metric-value" style="font-size:1.5rem;">{gain:,.0f} XAF</div></div>""", unsafe_allow_html=True)

                # Graphique flux
                dates_flux = [f"An {int(t/freq)}" if t % freq == 0 else f"S{t}" for t in range(1, n+1)]
                flux_vals = [coupon] * n
                flux_vals[-1] += valeur_nominale

                fig = go.Figure()
                fig.add_bar(x=dates_flux, y=flux_vals, name="Flux",
                    marker_color=["#C8A84B" if i < n-1 else "#003366" for i in range(n)])
                fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                    font=dict(family="Source Sans 3", size=11),
                    xaxis=dict(gridcolor="#EAE8E2"), yaxis=dict(gridcolor="#EAE8E2", title="XAF"),
                    height=250, margin=dict(l=0,r=0,t=10,b=0),
                    title="Échéancier des flux")
                st.plotly_chart(fig, use_container_width=True)

    # ── Tab 2 : Simulateur d'investissement ───────────────────────────────────
    with tab2:
        st.markdown("### Simulateur d'investissement")

        c1, c2 = st.columns(2)
        with c1:
            montant_inv = st.number_input("Montant à investir (XAF)", value=10_000_000, step=1_000_000, format="%d")
            taux_sim = st.slider("Taux de rendement (%)", 3.0, 12.0, 6.5, 0.1)
        with c2:
            horizon = st.slider("Horizon d'investissement (années)", 1, 15, 5)
            type_sim = st.selectbox("Type d'instrument", ["BTA","OTA coupon annuel","OTA coupon semestriel"])

        coupon_annuel = montant_inv * taux_sim / 100
        remboursement = montant_inv
        flux_list = []

        if type_sim == "BTA":
            nb_periodes = min(horizon, 1)
            flux_list = [(f"Période {i+1}", coupon_annuel * (13/52 if horizon <= 1 else 1)) for i in range(nb_periodes)]
            flux_list[-1] = (flux_list[-1][0], flux_list[-1][1] + remboursement)
        elif type_sim == "OTA coupon annuel":
            for i in range(1, horizon+1):
                f = coupon_annuel + (remboursement if i == horizon else 0)
                flux_list.append((f"An {i}", f))
        else:
            for i in range(1, horizon*2+1):
                f = coupon_annuel/2 + (remboursement if i == horizon*2 else 0)
                flux_list.append((f"S{i}", f))

        df_flux = pd.DataFrame(flux_list, columns=["Période","Flux (XAF)"])
        total = df_flux["Flux (XAF)"].sum()

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""<div class="metric-card"><div class="metric-label">Total flux perçus</div><div class="metric-value">{total/1_000_000:.2f} M XAF</div></div>""", unsafe_allow_html=True)
        with c2:
            revenus = total - montant_inv
            st.markdown(f"""<div class="metric-card"><div class="metric-label">Revenus nets</div><div class="metric-value">{revenus/1_000_000:.2f} M XAF</div></div>""", unsafe_allow_html=True)
        with c3:
            rdt_total = (revenus / montant_inv) * 100
            st.markdown(f"""<div class="metric-card"><div class="metric-label">Rendement total</div><div class="metric-value">{rdt_total:.2f} %</div></div>""", unsafe_allow_html=True)

        fig2 = go.Figure()
        fig2.add_bar(x=df_flux["Période"], y=df_flux["Flux (XAF)"],
            marker_color=["#003366" if i < len(df_flux)-1 else "#C8A84B" for i in range(len(df_flux))],
            name="Flux")
        fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Source Sans 3", size=11),
            xaxis=dict(gridcolor="#EAE8E2"), yaxis=dict(gridcolor="#EAE8E2", title="XAF"),
            height=280, margin=dict(l=0,r=0,t=10,b=0), title="Projection des flux de trésorerie")
        st.plotly_chart(fig2, use_container_width=True)

        csv = df_flux.to_csv(index=False).encode("utf-8")
        st.download_button(":material/download: Exporter la simulation", csv, "simulation.csv", key="dl_sim")

    # ── Tab 3 : Comparateur ───────────────────────────────────────────────────
    with tab3:
        st.markdown("### Comparateur d'instruments")
        st.markdown("Comparez jusqu'à 4 instruments selon différents critères.")

        nb_instruments = st.slider("Nombre d'instruments à comparer", 2, 4, 2)

        instruments = []
        cols = st.columns(nb_instruments)
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"**Instrument {i+1}**")
                instr = {
                    "label": st.text_input(f"Libellé", value=f"BTA {i+1}", key=f"lbl_{i}"),
                    "nominal": st.number_input("Nominal (M XAF)", value=10, key=f"nom_{i}"),
                    "taux": st.number_input("Taux (%)", value=round(4.0 + i*1.5, 1), key=f"taux_{i}"),
                    "duree": st.number_input("Durée (ans)", value=i+1, min_value=1, max_value=15, key=f"dur_{i}"),
                    "risque": st.select_slider("Risque relatif", options=["Faible","Modéré","Élevé"], key=f"rsk_{i}"),
                }
                instruments.append(instr)

        if st.button(":material/compare_arrows: Comparer", type="primary"):
            st.markdown("### Résultats de la comparaison")

            df_comp = pd.DataFrame([{
                "Instrument": inst["label"],
                "Nominal (M XAF)": inst["nominal"],
                "Taux (%)": inst["taux"],
                "Durée (ans)": inst["duree"],
                "Revenu total (M XAF)": round(inst["nominal"] * inst["taux"] / 100 * inst["duree"], 2),
                "Rendement/an": f"{inst['taux']:.1f}%",
                "Risque": inst["risque"],
            } for inst in instruments])

            st.dataframe(df_comp, use_container_width=True, hide_index=True)

            fig3 = go.Figure()
            for inst in instruments:
                revenu = inst["nominal"] * inst["taux"] / 100 * inst["duree"]
                fig3.add_bar(x=["Rendement (%)", "Revenu total (M XAF)", "Durée (ans)"],
                    y=[inst["taux"], revenu, inst["duree"]], name=inst["label"])
            fig3.update_layout(barmode="group", plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Source Sans 3"),
                height=300, margin=dict(l=0,r=0,t=10,b=0))
            st.plotly_chart(fig3, use_container_width=True)

            csv3 = df_comp.to_csv(index=False).encode("utf-8")
            st.download_button(":material/download: Exporter la comparaison", csv3, "comparaison.csv", key="dl_comp")
