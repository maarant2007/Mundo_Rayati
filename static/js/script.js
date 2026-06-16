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