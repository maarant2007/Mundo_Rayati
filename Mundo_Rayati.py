from flask import Flask, render_template_string, url_for
import os
app = Flask(__name__, static_folder='C:/MundoDeRayati/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

pagina = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>I.E.P. Mundo de Rayati</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Baloo+2:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --azul:    #1a7fc1;
    --azul-c:  #4fb3ef;
    --rojo:    #e8322a;
    --verde:   #3ab54a;
    --amarillo:#f5b800;
    --morado:  #9b3fbf;
    --naranja: #f47920;
    --blanco:  #ffffff;
    --gris-f:  #f4f8ff;
    --texto:   #2d3a4a;
  }

  * { margin:0; padding:0; box-sizing:border-box; }

  body {
    font-family: 'Nunito', sans-serif;
    background: var(--gris-f);
    color: var(--texto);
    overflow-x: hidden;
  }

  /* NAV */
  nav {
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--blanco);
    box-shadow: 0 2px 16px rgba(0,0,0,.10);
    padding: 0 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 70px;
  }
  .nav-logo {
    display: flex;
    align-items: center;
    text-decoration: none;
  }
  .nav-links {
    display: flex;
    gap: 8px;
    list-style: none;
    flex-wrap: wrap;
  }
  .nav-links a {
    text-decoration: none;
    font-weight: 700;
    font-size: 14px;
    color: var(--texto);
    padding: 8px 16px;
    border-radius: 30px;
    transition: background .2s, color .2s;
  }
  .nav-links a:hover {
    background: var(--azul);
    color: white;
  }
  .nav-links .btn-matricula {
    background: var(--rojo);
    color: white;
    border-radius: 30px;
    padding: 8px 20px;
  }
  .nav-links .btn-matricula:hover { background: var(--naranja); }

  /* HERO */
  .hero {
    position: relative;
    min-height: 92vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    overflow: hidden;
    background: linear-gradient(160deg, #dff4ff 0%, #fff7c9 50%, #ffe6f1 100%);
    padding: 60px 20px 80px;
  }
  .hero-bg {
    position: absolute;
    inset: 0;
    background-image: url("/static/imagenes/fondo.jpeg");
    background-size: cover;
    background-position: center;
    opacity: 0.18;
    z-index: 0;
  }
  .burbuja {
    position: absolute;
    border-radius: 50%;
    opacity: .18;
    animation: flotar 6s ease-in-out infinite;
  }
  .b1 { width:220px; height:220px; background:var(--azul-c);   top:-60px;   left:-60px;  animation-delay:0s; }
  .b2 { width:160px; height:160px; background:var(--amarillo); bottom:-40px; right:-40px; animation-delay:1.5s; }
  .b3 { width:100px; height:100px; background:var(--morado);   top:30%;     left:5%;     animation-delay:3s; }
  .b4 { width:80px;  height:80px;  background:var(--verde);    top:20%;     right:8%;    animation-delay:2s; }
  .b5 { width:120px; height:120px; background:var(--rojo);     bottom:10%;  left:15%;    animation-delay:4s; }

  @keyframes flotar {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-18px); }
  }

  .hero-content { position:relative; z-index:2; max-width:760px; }

  .hero-badge {
    display: inline-block;
    background: white;
    border: 2px solid var(--azul-c);
    color: var(--azul);
    font-weight: 800;
    font-size: 13px;
    padding: 6px 18px;
    border-radius: 30px;
    margin-bottom: 22px;
    letter-spacing: .5px;
    box-shadow: 0 2px 8px rgba(26,127,193,.15);
    animation: aparecer .7s ease both;
  }

  .hero h1 {
    font-family: 'Baloo 2', cursive;
    font-size: clamp(36px, 7vw, 72px);
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 12px;
    animation: aparecer .8s .1s ease both;
  }
  .hero h1 .txt-azul   { color: var(--azul); }
  .hero h1 .txt-rojo   { color: var(--rojo); }
  .hero h1 .txt-morado { color: var(--morado); }

  .hero p {
    font-size: 18px;
    color: #5a6a7a;
    margin-bottom: 34px;
    font-weight: 600;
    animation: aparecer .8s .2s ease both;
  }

  .hero-btns {
    display: flex;
    justify-content: center;
    gap: 14px;
    flex-wrap: wrap;
    animation: aparecer .8s .3s ease both;
  }

  .btn-primary {
    background: linear-gradient(135deg, var(--azul), var(--azul-c));
    color: white;
    font-weight: 800;
    font-size: 16px;
    padding: 14px 32px;
    border-radius: 40px;
    text-decoration: none;
    box-shadow: 0 6px 20px rgba(26,127,193,.35);
    transition: transform .2s, box-shadow .2s;
  }
  .btn-primary:hover { transform:translateY(-3px); box-shadow:0 10px 28px rgba(26,127,193,.45); }

  .btn-secondary {
    background: white;
    color: var(--rojo);
    border: 2px solid var(--rojo);
    font-weight: 800;
    font-size: 16px;
    padding: 14px 32px;
    border-radius: 40px;
    text-decoration: none;
    transition: background .2s, color .2s;
  }
  .btn-secondary:hover { background:var(--rojo); color:white; }

  @keyframes aparecer {
    from { opacity:0; transform:translateY(22px); }
    to   { opacity:1; transform:translateY(0); }
  }

  /* STATS BAR */
  .stats-bar {
    background: var(--azul);
    color: white;
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
  }
  .stat-item {
    padding: 22px 40px;
    text-align: center;
    border-right: 1px solid rgba(255,255,255,.2);
    flex: 1;
    min-width: 150px;
  }
  .stat-item:last-child { border-right:none; }
  .stat-item strong {
    display: block;
    font-family: 'Baloo 2', cursive;
    font-size: 32px;
    font-weight: 800;
  }
  .stat-item span { font-size: 13px; opacity:.85; font-weight:600; }

  /* SECCIONES */
  section { padding: 80px 20px; }
  .section-label {
    text-align: center;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--azul-c);
    margin-bottom: 10px;
  }
  .section-title {
    text-align: center;
    font-family: 'Baloo 2', cursive;
    font-size: clamp(26px, 4vw, 42px);
    font-weight: 800;
    color: var(--texto);
    margin-bottom: 12px;
  }
  .section-sub {
    text-align: center;
    font-size: 16px;
    color: #6a7a8a;
    max-width: 560px;
    margin: 0 auto 50px;
    font-weight: 600;
  }

  /* NIVELES */
  #niveles { background: white; }
  .niveles-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
    max-width: 960px;
    margin: 0 auto;
  }
  .nivel-card {
    border-radius: 22px;
    padding: 36px 28px;
    color: white;
    position: relative;
    overflow: hidden;
    transition: transform .25s, box-shadow .25s;
    box-shadow: 0 6px 24px rgba(0,0,0,.12);
  }
  .nivel-card:hover { transform:translateY(-6px); box-shadow:0 14px 36px rgba(0,0,0,.18); }
  .nivel-card.inicial  { background: linear-gradient(135deg, #f47920, #f5b800); }
  .nivel-card.primaria { background: linear-gradient(135deg, #1a7fc1, #4fb3ef); }
  .nivel-card.talleres { background: linear-gradient(135deg, #3ab54a, #a3d977); }
  .nivel-card .nivel-icon { font-size: 48px; margin-bottom: 16px; display: block; }
  .nivel-card h3 {
    font-family: 'Baloo 2', cursive;
    font-size: 26px;
    font-weight: 800;
    margin-bottom: 10px;
  }
  .nivel-card p { font-size: 15px; opacity:.92; font-weight:600; line-height:1.6; }
  .nivel-card .nivel-tag {
    display: inline-block;
    background: rgba(255,255,255,.25);
    font-size: 12px;
    font-weight: 800;
    padding: 4px 12px;
    border-radius: 20px;
    margin-top: 18px;
    letter-spacing:.5px;
  }

  /* POR QUE ELEGIRNOS */
  #porque { background: var(--gris-f); }
  .razones-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 20px;
    max-width: 1000px;
    margin: 0 auto;
  }
  .razon-card {
    background: white;
    border-radius: 18px;
    padding: 30px 24px;
    box-shadow: 0 3px 14px rgba(0,0,0,.07);
    border-top: 5px solid;
    transition: transform .2s;
  }
  .razon-card:hover { transform:translateY(-4px); }
  .razon-card:nth-child(1) { border-color: var(--azul); }
  .razon-card:nth-child(2) { border-color: var(--rojo); }
  .razon-card:nth-child(3) { border-color: var(--verde); }
  .razon-card:nth-child(4) { border-color: var(--amarillo); }
  .razon-card:nth-child(5) { border-color: var(--morado); }
  .razon-card:nth-child(6) { border-color: var(--naranja); }
  .razon-icon { font-size: 36px; margin-bottom: 14px; }
  .razon-card h3 {
    font-family: 'Baloo 2', cursive;
    font-size: 18px;
    font-weight: 800;
    color: var(--texto);
    margin-bottom: 8px;
  }
  .razon-card p { font-size: 14px; color:#6a7a8a; font-weight:600; line-height:1.6; }

  /* VALORES */
  #valores { background: linear-gradient(135deg, #1a7fc1 0%, #9b3fbf 100%); }
  #valores .section-label { color: #a3d4ff; }
  #valores .section-title { color: white; }
  #valores .section-sub   { color: rgba(255,255,255,.8); }
  .valores-grid {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 16px;
    max-width: 800px;
    margin: 0 auto;
  }
  .valor-pill {
    background: rgba(255,255,255,.15);
    border: 2px solid rgba(255,255,255,.3);
    color: white;
    padding: 12px 24px;
    border-radius: 40px;
    font-size: 16px;
    font-weight: 700;
    transition: background .2s;
  }
  .valor-pill:hover { background: rgba(255,255,255,.3); }

  /* ===================== TIENDA ===================== */
  #tienda { background: white; }
  #tienda .section-label { color: var(--verde); }

  .tienda-tabs {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 40px;
  }
  .tab-btn {
    background: var(--gris-f);
    border: 2px solid transparent;
    color: var(--texto);
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 14px;
    padding: 10px 22px;
    border-radius: 30px;
    cursor: pointer;
    transition: all .2s;
  }
  .tab-btn:hover, .tab-btn.active {
    background: var(--azul);
    color: white;
    border-color: var(--azul);
  }

  .productos-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
    gap: 22px;
    max-width: 1050px;
    margin: 0 auto;
  }
  .producto-card {
    background: var(--gris-f);
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 3px 14px rgba(0,0,0,.07);
    transition: transform .25s, box-shadow .25s;
    display: none;
  }
  .producto-card.visible { display: flex; flex-direction: column; }
  .producto-card:hover { transform:translateY(-5px); box-shadow:0 12px 32px rgba(0,0,0,.13); }

  .prod-emoji {
    font-size: 56px;
    text-align: center;
    padding: 28px 20px 14px;
    background: white;
    line-height: 1;
  }
  .prod-body { padding: 18px 20px 22px; flex:1; display:flex; flex-direction:column; }
  .prod-cat {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  .prod-cat.libros    { color: var(--azul); }
  .prod-cat.uniforme  { color: var(--verde); }
  .prod-cat.agendas   { color: var(--morado); }

  .prod-body h4 {
    font-family: 'Baloo 2', cursive;
    font-size: 17px;
    font-weight: 800;
    color: var(--texto);
    margin-bottom: 6px;
    line-height: 1.3;
  }
  .prod-body p { font-size: 13px; color:#6a7a8a; font-weight:600; line-height:1.5; flex:1; margin-bottom:14px; }

  .prod-precio-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: auto;
  }
  .prod-precio {
    font-family: 'Baloo 2', cursive;
    font-size: 20px;
    font-weight: 800;
    color: var(--rojo);
  }
  .btn-pedir {
    background: linear-gradient(135deg, var(--verde), #6dd67a);
    color: white;
    border: none;
    padding: 8px 18px;
    border-radius: 20px;
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 13px;
    cursor: pointer;
    text-decoration: none;
    transition: opacity .2s, transform .2s;
    display: inline-block;
  }
  .btn-pedir:hover { opacity:.88; transform:translateY(-1px); }

  .tienda-nota {
    text-align: center;
    font-size: 14px;
    color: #8a9aaa;
    font-weight: 600;
    margin-top: 36px;
    max-width: 560px;
    margin-left: auto;
    margin-right: auto;
  }
  .tienda-nota strong { color: var(--azul); }

  /* ===================== MATRÍCULA ===================== */
  #matricula { background: linear-gradient(160deg, #fff7e6 0%, #ffe8e8 100%); }
  #matricula .section-label { color: var(--naranja); }

  .matricula-wrap {
    max-width: 700px;
    margin: 0 auto;
  }

  /* Pasos del proceso */
  .pasos-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 48px;
  }
  .paso-card {
    background: white;
    border-radius: 18px;
    padding: 24px 20px;
    text-align: center;
    box-shadow: 0 3px 14px rgba(0,0,0,.07);
    position: relative;
  }
  .paso-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    background: var(--rojo);
    color: white;
    border-radius: 50%;
    font-weight: 900;
    font-size: 16px;
    margin-bottom: 12px;
  }
  .paso-card .paso-icon { font-size: 30px; display: block; margin-bottom: 10px; }
  .paso-card h4 {
    font-family: 'Baloo 2', cursive;
    font-size: 15px;
    font-weight: 800;
    color: var(--texto);
    margin-bottom: 6px;
  }
  .paso-card p { font-size: 12px; color: #7a8a9a; font-weight: 600; line-height: 1.5; }

  /* Formulario de matrícula */
  .matricula-form {
    background: white;
    border-radius: 24px;
    padding: 44px 40px;
    box-shadow: 0 4px 24px rgba(0,0,0,.08);
    border-top: 5px solid var(--rojo);
  }
  .matricula-form .form-titulo {
    font-family: 'Baloo 2', cursive;
    font-size: 22px;
    font-weight: 800;
    color: var(--texto);
    margin-bottom: 6px;
  }
  .matricula-form .form-subtitulo {
    font-size: 14px;
    color: #8a9aaa;
    font-weight: 600;
    margin-bottom: 28px;
  }
  .form-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  @media (max-width: 560px) { .form-grid-2 { grid-template-columns: 1fr; } }

  .form-row { margin-bottom: 18px; }
  .form-row label {
    display: block;
    font-weight: 700;
    font-size: 14px;
    color: var(--texto);
    margin-bottom: 6px;
  }
  .form-row input,
  .form-row select,
  .form-row textarea {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #d8e6f3;
    border-radius: 12px;
    font-family: 'Nunito', sans-serif;
    font-size: 15px;
    color: var(--texto);
    background: white;
    outline: none;
    transition: border .2s;
  }
  .form-row input:focus,
  .form-row select:focus,
  .form-row textarea:focus { border-color: var(--rojo); }
  .form-row textarea { resize: vertical; min-height: 100px; }

  .btn-matricula-form {
    width: 100%;
    background: linear-gradient(135deg, var(--rojo), var(--naranja));
    color: white;
    border: none;
    padding: 15px;
    border-radius: 12px;
    font-family: 'Nunito', sans-serif;
    font-size: 17px;
    font-weight: 800;
    cursor: pointer;
    transition: opacity .2s, transform .2s;
    margin-top: 8px;
  }
  .btn-matricula-form:hover { opacity:.9; transform:translateY(-2px); }

  .matricula-requisitos {
    background: #fff4e6;
    border: 2px solid #ffd199;
    border-radius: 16px;
    padding: 20px 24px;
    margin-top: 28px;
  }
  .matricula-requisitos h4 {
    font-family: 'Baloo 2', cursive;
    font-size: 16px;
    font-weight: 800;
    color: var(--naranja);
    margin-bottom: 12px;
  }
  .matricula-requisitos ul {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .matricula-requisitos ul li {
    font-size: 13px;
    font-weight: 600;
    color: #6a5a4a;
  }
  .matricula-requisitos ul li::before {
    content: "✅ ";
  }

  /* ===================== CONTACTO ===================== */
  #contacto { background: var(--gris-f); }

  .contacto-grid {
    display: grid;
    grid-template-columns: 1fr 1.4fr;
    gap: 32px;
    max-width: 900px;
    margin: 0 auto;
    align-items: start;
  }
  @media (max-width: 700px) { .contacto-grid { grid-template-columns: 1fr; } }

  /* Panel de info de contacto */
  .contacto-info {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .info-card {
    background: white;
    border-radius: 18px;
    padding: 22px 24px;
    box-shadow: 0 3px 14px rgba(0,0,0,.07);
    display: flex;
    align-items: flex-start;
    gap: 14px;
  }
  .info-card .info-icon {
    font-size: 28px;
    flex-shrink: 0;
    margin-top: 2px;
  }
  .info-card h4 {
    font-family: 'Baloo 2', cursive;
    font-size: 16px;
    font-weight: 800;
    color: var(--texto);
    margin-bottom: 4px;
  }
  .info-card p, .info-card a {
    font-size: 13px;
    font-weight: 600;
    color: #6a7a8a;
    text-decoration: none;
    line-height: 1.6;
  }
  .info-card a:hover { color: var(--azul); }

  .btn-whatsapp {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    background: #25d366;
    color: white;
    font-weight: 800;
    font-size: 15px;
    padding: 14px 24px;
    border-radius: 14px;
    text-decoration: none;
    box-shadow: 0 4px 16px rgba(37,211,102,.30);
    transition: transform .2s, box-shadow .2s;
  }
  .btn-whatsapp:hover { transform:translateY(-2px); box-shadow:0 8px 24px rgba(37,211,102,.40); }

  /* Formulario de contacto */
  .contacto-form {
    background: white;
    border-radius: 24px;
    padding: 40px 36px;
    box-shadow: 0 4px 24px rgba(0,0,0,.08);
    border-top: 5px solid var(--azul);
  }
  .contacto-form .form-titulo {
    font-family: 'Baloo 2', cursive;
    font-size: 20px;
    font-weight: 800;
    color: var(--texto);
    margin-bottom: 4px;
  }
  .contacto-form .form-subtitulo {
    font-size: 13px;
    color: #8a9aaa;
    font-weight: 600;
    margin-bottom: 24px;
  }

  .btn-form-contacto {
    width: 100%;
    background: linear-gradient(135deg, var(--azul), var(--azul-c));
    color: white;
    border: none;
    padding: 14px;
    border-radius: 12px;
    font-family: 'Nunito', sans-serif;
    font-size: 16px;
    font-weight: 800;
    cursor: pointer;
    transition: opacity .2s, transform .2s;
    margin-top: 6px;
  }
  .btn-form-contacto:hover { opacity:.9; transform:translateY(-2px); }

  /* FOOTER */
  footer {
    background: var(--texto);
    color: white;
    padding: 40px 30px 24px;
  }
  .footer-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 28px;
    max-width: 960px;
    margin: 0 auto 28px;
  }
  .footer-brand .brand-name {
    font-family: 'Baloo 2', cursive;
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 6px;
  }
  .footer-brand p { font-size:13px; opacity:.65; max-width:220px; line-height:1.6; }
  .footer-col h4 { font-size:14px; font-weight:800; margin-bottom:12px; opacity:.9; }
  .footer-col ul { list-style:none; }
  .footer-col ul li { margin-bottom:8px; }
  .footer-col ul li a { color:rgba(255,255,255,.65); text-decoration:none; font-size:13px; font-weight:600; transition:color .2s; }
  .footer-col ul li a:hover { color:var(--azul-c); }
  .footer-bottom {
    text-align:center;
    font-size:12px;
    opacity:.5;
    border-top:1px solid rgba(255,255,255,.1);
    padding-top:18px;
    max-width:960px;
    margin:0 auto;
  }

  /* BARRA ARCOIRIS */
  .rainbow-bar {
    height: 6px;
    background: linear-gradient(90deg,
      #e8322a 0%, #f47920 17%, #f5b800 33%,
      #3ab54a 50%, #1a7fc1 67%, #4fb3ef 83%, #9b3fbf 100%
    );
  }
</style>
</head>
<body>

<div class="rainbow-bar"></div>

<!-- NAV -->
<nav>
  <a href="#" class="nav-logo">
    <img src="/static/imagenes/logo.jpeg" alt="Mundo de Rayati" style="height:54px; width:auto;">
    <span style="font-family:'Baloo 2',cursive;font-weight:800;font-size:20px;color:var(--azul);margin-left:10px;">Mundo de Rayati</span>
  </a>
  <ul class="nav-links">
    <li><a href="#niveles">Niveles</a></li>
    <li><a href="#porque">¿Por qué?</a></li>
    <li><a href="#tienda">Tienda</a></li>
    <li><a href="#contacto">Contacto</a></li>
    <li><a href="#matricula" class="btn-matricula">Matrícula 2026</a></li>
  </ul>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-bg"></div>
  <div class="burbuja b1"></div>
  <div class="burbuja b2"></div>
  <div class="burbuja b3"></div>
  <div class="burbuja b4"></div>
  <div class="burbuja b5"></div>
  <div class="hero-content">
    <span class="hero-badge">✨ Institución Educativa Particular</span>
    <h1>
      <span class="txt-azul">Mundo</span>
      <span class="txt-amarillo"> de  </span>
      <span class="txt-rojo">Ray</span><span class="txt-morado">ati</span>
    </h1>
    <div class="hero-btns">
      <a href="#niveles" class="btn-primary">Conoce nuestros niveles</a>
      <a href="#matricula" class="btn-secondary">Matrícula 2026</a>
    </div>
  </div>
</section>

<!-- STATS BAR -->
<div class="stats-bar">
  <div class="stat-item"><strong>15+</strong><span>Años de experiencia</span></div>
  <div class="stat-item"><strong>500+</strong><span>Alumnos felices</span></div>
  <div class="stat-item"><strong>30+</strong><span>Docentes calificados</span></div>
  <div class="stat-item"><strong>100%</strong><span>Compromiso familiar</span></div>
</div>

<!-- NIVELES -->
<section id="niveles">
  <p class="section-label">Nuestros programas</p>
  <h2 class="section-title">Niveles educativos</h2>
  <p class="section-sub">Acompañamos a tu hijo en cada etapa de su desarrollo con programas diseñados para brillar.</p>
  <div class="niveles-grid">
    <div class="nivel-card inicial">
      <span class="nivel-icon">🌱</span>
      <h3>Nivel Inicial</h3>
      <p>3, 4 y 5 años. Aprendizaje lúdico, desarrollo emocional y primeras habilidades sociales en un ambiente cálido y seguro.</p>
      <span class="nivel-tag">3 – 5 años</span>
    </div>
    <div class="nivel-card primaria">
      <span class="nivel-icon">📚</span>
      <h3>Nivel Primaria</h3>
      <p>1° a 6° grado. Formación académica sólida, pensamiento crítico y valores que los preparan para el futuro.</p>
      <span class="nivel-tag">6 – 12 años</span>
    </div>
    <div class="nivel-card talleres">
      <span class="nivel-icon">🎨</span>
      <h3>Talleres</h3>
      <p>Arte, música, deporte y robótica. Potenciamos el talento único de cada niño más allá del aula.</p>
      <span class="nivel-tag">Extracurricular</span>
    </div>
  </div>
</section>

<!-- POR QUÉ ELEGIRNOS -->
<section id="porque">
  <p class="section-label">Nuestras fortalezas</p>
  <h2 class="section-title">¿Por qué elegirnos?</h2>
  <p class="section-sub">Más que una escuela: una comunidad comprometida con el bienestar y el aprendizaje de tus hijos.</p>
  <div class="razones-grid">
    <div class="razon-card">
      <div class="razon-icon">👩‍🏫</div>
      <h3>Docentes vocacionales</h3>
      <p>Maestros certificados y apasionados por la educación infantil, en constante capacitación.</p>
    </div>
    <div class="razon-card">
      <div class="razon-icon">🏫</div>
      <h3>Infraestructura moderna</h3>
      <p>Ambientes amplios, seguros y estimulantes diseñados pensando en los niños.</p>
    </div>
    <div class="razon-card">
      <div class="razon-icon">💡</div>
      <h3>Metodología activa</h3>
      <p>Aprendizaje basado en proyectos, juego y experiencias significativas.</p>
    </div>
    <div class="razon-card">
      <div class="razon-icon">🤝</div>
      <h3>Comunidad y familia</h3>
      <p>Padres involucrados como aliados del proceso educativo de sus hijos.</p>
    </div>
    <div class="razon-card">
      <div class="razon-icon">🎯</div>
      <h3>Atención personalizada</h3>
      <p>Grupos reducidos para garantizar seguimiento individual a cada estudiante.</p>
    </div>
    <div class="razon-card">
      <div class="razon-icon">🌈</div>
      <h3>Valores y convivencia</h3>
      <p>Formamos ciudadanos íntegros con sólidos principios éticos y respeto mutuo.</p>
    </div>
  </div>
</section>

<!-- VALORES -->
<section id="valores">
  <p class="section-label">Lo que nos define</p>
  <h2 class="section-title">Nuestros valores</h2>
  <p class="section-sub">Principios que guían cada acción dentro y fuera del aula.</p>
  <div class="valores-grid">
    <span class="valor-pill">🧡 Amor</span>
    <span class="valor-pill">🌟 Excelencia</span>
    <span class="valor-pill">🤝 Respeto</span>
    <span class="valor-pill">💪 Responsabilidad</span>
    <span class="valor-pill">🌱 Crecimiento</span>
    <span class="valor-pill">🎨 Creatividad</span>
    <span class="valor-pill">🌍 Inclusión</span>
    <span class="valor-pill">😊 Alegría</span>
  </div>
</section>

<!-- ===================== TIENDA ===================== -->
<section id="tienda">
  <p class="section-label">Tienda Escolar</p>
  <h2 class="section-title">📦 Libros, Uniformes y Útiles</h2>
  <p class="section-sub">Encuentra todo lo que tu hijo necesita para el año escolar, con precios accesibles y calidad garantizada.</p>

  <div class="tienda-tabs">
    <button class="tab-btn active" onclick="filtrar(this,'todos')">🛒 Todo</button>
    <button class="tab-btn" onclick="filtrar(this,'libros')">📚 Libros</button>
    <button class="tab-btn" onclick="filtrar(this,'uniforme')">👕 Uniformes</button>
    <button class="tab-btn" onclick="filtrar(this,'agendas')">📓 Agenda</button>
  </div>

  <div class="productos-grid">

    <!-- LIBROS -->
    <div class="producto-card visible" data-cat="libros">
      <div class="prod-emoji">📖</div>
      <div class="prod-body">
        <span class="prod-cat libros">Libros</span>
        <h4>Comunicación – Nivel Inicial</h4>
        <p>Libro de trabajo para 3, 4 y 5 años. Incluye fichas de lectoescritura y comprensión lectora.</p>
        <div class="prod-precio-row">
          <span class="prod-precio">S/ 35.00</span>
          <a href="#contacto" class="btn-pedir">Pedir</a>
        </div>
      </div>
    </div>

    <div class="producto-card visible" data-cat="libros">
      <div class="prod-emoji">🔢</div>
      <div class="prod-body">
        <span class="prod-cat libros">Libros</span>
        <h4>Matemática – Nivel Inicial</h4>
        <p>Cuaderno de ejercicios numéricos, lógica y geometría básica para inicial.</p>
        <div class="prod-precio-row">
          <span class="prod-precio">S/ 32.00</span>
          <a href="#contacto" class="btn-pedir">Pedir</a>
        </div>
      </div>
    </div>

    <div class="producto-card visible" data-cat="libros">
      <div class="prod-emoji">📘</div>
      <div class="prod-body">
        <span class="prod-cat libros">Libros</span>
        <h4>Comunicación – Primaria (1° – 3°)</h4>
        <p>Libro oficial de Comunicación para los primeros grados de primaria. Comprensión y producción de textos.</p>
        <div class="prod-precio-row">
          <span class="prod-precio">S/ 42.00</span>
          <a href="#contacto" class="btn-pedir">Pedir</a>
        </div>
      </div>
    </div>

    <div class="producto-card visible" data-cat="libros">
      <div class="prod-emoji">📗</div>
      <div class="prod-body">
        <span class="prod-cat libros">Libros</span>
        <h4>Matemática – Primaria (1° – 3°)</h4>
        <p>Libro de Matemática con ejercicios progresivos, problemas y actividades lúdicas.</p>
        <div class="prod-precio-row">
          <span class="prod-precio">S/ 42.00</span>
          <a href="#contacto" class="btn-pedir">Pedir</a>
        </div>
      </div>
    </div>

    <div class="producto-card visible" data-cat="libros">
      <div class="prod-emoji">📙</div>
      <div class="prod-body">
        <span class="prod-cat libros">Libros</span>
        <h4>Comunicación – Primaria (4° – 6°)</h4>
        <p>Libro de Comunicación para grados superiores. Literatura, gramática y ortografía.</p>
        <div class="prod-precio-row">
          <span class="prod-precio">S/ 45.00</span>
          <a href="#contacto" class="btn-pedir">Pedir</a>
        </div>
      </div>
    </div>

    <div class="producto-card visible" data-cat="libros">
      <div class="prod-emoji">📕</div>
      <div class="prod-body">
        <span class="prod-cat libros">Libros</span>
        <h4>Matemática – Primaria (4° – 6°)</h4>
        <p>Matemática avanzada con fracciones, álgebra básica y resolución de problemas.</p>
        <div class="prod-precio-row">
          <span class="prod-precio">S/ 45.00</span>
          <a href="#contacto" class="btn-pedir">Pedir</a>
        </div>
      </div>
    </div>

    <!-- UNIFORMES -->
    <div class="producto-card visible" data-cat="uniforme">
      <div class="prod-emoji">👕</div>
      <div class="prod-body">
        <span class="prod-cat uniforme">Uniforme</span>
        <h4>Polo Colegio</h4>
        <p>Polo oficial con logo bordado del colegio. Tallas: 2, 4, 6, 8, 10, 12, 14. Colores: blanco y azul.</p>
        <div class="prod-precio-row">
          <span class="prod-precio">S/ 28.00</span>
          <a href="#contacto" class="btn-pedir">Pedir</a>
        </div>
      </div>
    </div>

    <div class="producto-card visible" data-cat="uniforme">
      <div class="prod-emoji">🧥</div>
      <div class="prod-body">
        <span class="prod-cat uniforme">Uniforme</span>
        <h4>Buzo Completo (casaca + pantalón)</h4>
        <p>Buzo deportivo oficial azul marino con detalles en rojo. Tallas: 2 al 14. Tela antifluido y cómoda.</p>
        <div class="prod-precio-row">
          <span class="prod-precio">S/ 85.00</span>
          <a href="#contacto" class="btn-pedir">Pedir</a>
        </div>
      </div>
    </div>

    <div class="producto-card visible" data-cat="uniforme">
      <div class="prod-emoji">🩳</div>
      <div class="prod-body">
        <span class="prod-cat uniforme">Uniforme</span>
        <h4>Short Educación Física</h4>
        <p>Short deportivo para clases de educación física. Tela ligera y transpirable. Azul marino con logo.</p>
        <div class="prod-precio-row">
          <span class="prod-precio">S/ 25.00</span>
          <a href="#contacto" class="btn-pedir">Pedir</a>
        </div>
      </div>
    </div>

    <!-- AGENDA ÚNICA -->
    <div class="producto-card visible" data-cat="agendas">
      <div class="prod-emoji">📓</div>
      <div class="prod-body">
        <span class="prod-cat agendas">Agenda</span>
        <h4>Agenda Escolar Mundo de Rayati</h4>
        <p>Agenda oficial única para todo el colegio (Inicial y Primaria). Incluye horario semanal, registro de tareas, calendario escolar anual y espacio para comunicados a los padres.</p>
        <div class="prod-precio-row">
          <span class="prod-precio">S/ 20.00</span>
          <a href="#contacto" class="btn-pedir">Pedir</a>
        </div>
      </div>
    </div>

  </div>

  <p class="tienda-nota">
    💬 Para realizar tu pedido, escríbenos por <strong>WhatsApp o al formulario de contacto</strong>.<br>
    Entrega en institución o coordina el recojo. Precios válidos para la campaña escolar 2025.
  </p>
</section>

<!-- ===================== MATRÍCULA ===================== -->
<section id="matricula">
  <p class="section-label">Inscripciones 2026</p>
  <h2 class="section-title">🎒 Proceso de Matrícula</h2>
  <p class="section-sub">Asegura el cupo de tu hijo en pocos pasos. Las vacantes son limitadas.</p>

  <div class="matricula-wrap">

    <!-- Pasos -->
    <div class="pasos-grid">
      <div class="paso-card">
        <span class="paso-num">1</span>
        <span class="paso-icon">📋</span>
        <h4>Solicita información</h4>
        <p>Completa el formulario y nos comunicamos contigo en menos de 24 h.</p>
      </div>
      <div class="paso-card">
        <span class="paso-num">2</span>
        <span class="paso-icon">🏫</span>
        <h4>Visita el colegio</h4>
        <p>Conoce nuestras instalaciones y conversa con nuestra directora.</p>
      </div>
      <div class="paso-card">
        <span class="paso-num">3</span>
        <span class="paso-icon">📄</span>
        <h4>Entrega documentos</h4>
        <p>Presenta los requisitos indicados y realiza el pago de matrícula.</p>
      </div>
      <div class="paso-card">
        <span class="paso-num">4</span>
        <span class="paso-icon">🎉</span>
        <h4>¡Bienvenido!</h4>
        <p>Tu hijo ya es parte de la familia Mundo de Rayati.</p>
      </div>
    </div>

    <!-- Formulario -->
    <div class="matricula-form">
      <p class="form-titulo">📝 Solicitud de matrícula</p>
      <p class="form-subtitulo">Completa el formulario y te contactamos para coordinar tu visita.</p>

      <div class="form-grid-2">
        <div class="form-row">
          <label>Nombre del apoderado</label>
          <input type="text" placeholder="Nombre completo">
        </div>
        <div class="form-row">
          <label>Teléfono / WhatsApp</label>
          <input type="tel" placeholder="+51 945373930">
        </div>
      </div>

      <div class="form-grid-2">
        <div class="form-row">
          <label>Nombre del alumno</label>
          <input type="text" placeholder="Nombre del niño/a">
        </div>
        <div class="form-row">
          <label>Edad del alumno</label>
          <input type="number" placeholder="Ej: 5" min="3" max="13">
        </div>
      </div>

      <div class="form-row">
        <label>Nivel al que postula</label>
        <select>
         <option>Inicial – 2 años</option>
          <option>Inicial – 3 años</option>
          <option>Inicial – 4 años</option>
          <option>Inicial – 5 años</option>
          <option>Primaria – 1° grado</option>
          <option>Primaria – 2° grado</option>
          <option>Primaria – 3° grado</option>
          <option>Primaria – 4° grado</option>
          <option>Primaria – 5° grado</option>
          <option>Primaria – 6° grado</option>
        </select>
      </div>

      <div class="form-row">
        <label>Comentarios adicionales</label>
        <textarea placeholder="¿Tienes alguna consulta sobre el proceso de matrícula?"></textarea>
      </div>

      <button class="btn-matricula-form">Enviar solicitud de matrícula 🎒</button>

      <!-- Requisitos -->
      <div class="matricula-requisitos">
        <h4>📋 Documentos requeridos</h4>
        <ul>
          <li>Partida de nacimiento (copia)</li>
          <li>DNI del alumno (si aplica)</li>
          <li>DNI del apoderado (copia)</li>
          <li>Libreta de notas del año anterior</li>
          <li>2 fotografías tamaño carné</li>
          <li>Ficha de salud actualizada</li>
        </ul>
      </div>
    </div>

  </div>
</section>

<!-- ===================== CONTACTO ===================== -->
<section id="contacto">
  <p class="section-label">Comunícate con nosotros</p>
  <h2 class="section-title">📬 Contáctanos</h2>
  <p class="section-sub">¿Tienes dudas sobre la tienda, talleres u otra consulta general? Escríbenos directamente.</p>

  <div class="contacto-grid">

    <!-- Info de contacto -->
    <div class="contacto-info">
      <div class="info-card">
        <span class="info-icon">📍</span>
        <div>
          <h4>Dirección</h4>
          <p>Av. Los Niños 123, Urb. Las Flores<br>Lima, Perú</p>
        </div>
      </div>
      <div class="info-card">
        <span class="info-icon">🕐</span>
        <div>
          <h4>Horario de atención</h4>
          <p>Lunes a Viernes: 7:30 am – 5:00 pm<br>Sábados: 8:00 am – 12:00 pm</p>
        </div>
      </div>
      <div class="info-card">
        <span class="info-icon">📞</span>
        <div>
          <h4>Teléfono</h4>
          <p>(01) 234-5678<br>
          <a href="tel:+51945373930">+51 945373930</a></p>
        </div>
      </div>
      <div class="info-card">
        <span class="info-icon">✉️</span>
        <div>
          <h4>Correo electrónico</h4>
          <a href="mailto:info@mundoderayati.edu.pe">info@mundoderayati.edu.pe</a>
        </div>
      </div>
      <a href="https://wa.me/51945373930" class="btn-whatsapp" target="_blank">
        💬 Escribir por WhatsApp
      </a>
    </div>

    <!-- Formulario de contacto -->
    <div class="contacto-form">
      <p class="form-titulo">Envíanos un mensaje</p>
      <p class="form-subtitulo">Te respondemos en menos de 24 horas hábiles.</p>

      <div class="form-row">
        <label>Nombre completo</label>
        <input type="text" placeholder="Tu nombre">
      </div>
      <div class="form-row">
        <label>Teléfono / WhatsApp</label>
        <input type="tel" placeholder="+51 945373930">
      </div>
      <div class="form-row">
        <label>Motivo de consulta</label>
        <select>
          <option>Consulta sobre la tienda escolar</option>
          <option>Información sobre talleres</option>
          <option>Consulta sobre pagos y pensiones</option>
          <option>Otro</option>
        </select>
      </div>
      <div class="form-row">
        <label>Mensaje</label>
        <textarea placeholder="Escribe tu consulta aquí…"></textarea>
      </div>
      <button class="btn-form-contacto">Enviar mensaje ✉️</button>
    </div>

  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="footer-top">
    <div class="footer-brand">
      <img src="/static/imagenes/logo.jpeg" alt="Mundo de Rayati" style="height:64px; width:auto; margin-bottom:10px; filter: brightness(0) invert(1);">
      <p>Formando con amor, educando para la vida. I.E.P. comprometida con la excelencia.</p>
    </div>
    <div class="footer-col">
      <h4>Institución</h4>
      <ul>
        <li><a href="#niveles">Niveles educativos</a></li>
        <li><a href="#porque">¿Por qué elegirnos?</a></li>
        <li><a href="#valores">Nuestros valores</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Tienda</h4>
      <ul>
        <li><a href="#tienda">Libros</a></li>
        <li><a href="#tienda">Uniformes</a></li>
        <li><a href="#tienda">Agenda</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Institución</h4>
      <ul>
        <li><a href="#matricula">Matrícula 2026</a></li>
        <li><a href="#contacto">Contacto general</a></li>
        <li><a href="https://wa.me/51945373930">WhatsApp</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    © 2025 I.E.P. Mundo de Rayati · Todos los derechos reservados
  </div>
</footer>

<div class="rainbow-bar"></div>

<script>
  function filtrar(btn, cat) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.producto-card').forEach(card => {
      if (cat === 'todos' || card.dataset.cat === cat) {
        card.classList.add('visible');
      } else {
        card.classList.remove('visible');
      }
    });
  }
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(pagina)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=False)
