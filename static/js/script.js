function filtrar(btn, cat) {
  // Quita la clase 'active' de todos los botones de las pestañas
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));

  // Agrega la clase 'active' al botón que acaba de ser presionado
  btn.classList.add('active');

  // Recorre todas las tarjetas de productos para mostrarlas u ocultarlas
  document.querySelectorAll('.producto-card').forEach(card => {
    if (cat === 'todos' || card.dataset.cat === cat) {
      card.classList.add('visible');
    } else {
      card.classList.remove('visible');
    }
  });
}

/* ============================
   MENÚ HAMBURGUESA (móvil)
   ============================ */
function toggleNav() {
  document.getElementById('navLinks').classList.toggle('open');
  document.getElementById('navToggle').classList.toggle('open');
}

// Cierra el menú automáticamente al tocar un link (mejor experiencia en móvil)
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    document.getElementById('navLinks').classList.remove('open');
    document.getElementById('navToggle').classList.remove('open');
  });
});