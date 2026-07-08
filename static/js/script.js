/* ============================
   TIENDA — filtro de categorías
   ============================ */
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

/* ============================
   MENÚ HAMBURGUESA (móvil)
   ============================ */
function toggleNav() {
  document.getElementById('navLinks').classList.toggle('open');
  document.getElementById('navToggle').classList.toggle('open');
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
      document.getElementById('navLinks').classList.remove('open');
      document.getElementById('navToggle').classList.remove('open');
    });
  });
});


/* ============================================================
   VALIDACIÓN GENÉRICA DE FORMULARIOS
   ============================================================ */
function validarCampos(mapaCampos) {
  const faltantes = [];
  Object.entries(mapaCampos).forEach(([id, etiqueta]) => {
    const el = document.getElementById(id);
    const errEl = document.getElementById(id + '-err');
    if (!el) return;
    const valor = (el.value || '').toString().trim();
    if (valor === '') {
      el.classList.add('input-error');
      if (errEl) errEl.textContent = 'Este campo es obligatorio';
      faltantes.push(etiqueta);
    } else {
      el.classList.remove('input-error');
      if (errEl) errEl.textContent = '';
    }
  });
  return faltantes;
}

function mostrarMensajeForm(idMsg, texto, esError) {
  const box = document.getElementById(idMsg);
  if (!box) return;
  box.textContent = texto;
  box.classList.remove('success', 'error');
  box.classList.add('show', esError ? 'error' : 'success');
}

function ocultarMensajeForm(idMsg) {
  const box = document.getElementById(idMsg);
  if (box) box.classList.remove('show');
}


/* ============================================================
   FORMULARIO PÚBLICO: MATRÍCULA
   ============================================================ */
async function enviarMatricula() {
  ocultarMensajeForm('matricula-msg');

  const faltantes = validarCampos({
    'mp-apoderado': 'Nombre del apoderado',
    'mp-telefono': 'Teléfono',
    'mp-alumno': 'Nombre del alumno',
    'mp-edad': 'Edad del alumno',
    'mp-nivel': 'Nivel al que postula'
  });

  if (faltantes.length) {
    mostrarMensajeForm('matricula-msg', 'Por favor completa todos los campos obligatorios (*) antes de enviar.', true);
    document.getElementById('matricula-msg').scrollIntoView({ behavior: 'smooth', block: 'center' });
    return;
  }

  const payload = {
    apoderado: document.getElementById('mp-apoderado').value.trim(),
    telefono: document.getElementById('mp-telefono').value.trim(),
    alumno: document.getElementById('mp-alumno').value.trim(),
    edad: parseInt(document.getElementById('mp-edad').value),
    nivel: document.getElementById('mp-nivel').value,
    comentarios: document.getElementById('mp-comentarios').value.trim(),
  };

  const btn = document.getElementById('mp-submit-btn');
  btn.disabled = true;
  btn.textContent = 'Enviando...';

  try {
    const res = await fetch('/api/matricula-publica', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (!res.ok) {
      mostrarMensajeForm('matricula-msg', 'Faltan datos: ' + (data.campos || []).join(', '), true);
      return;
    }

    mostrarMensajeForm('matricula-msg', data.mensaje || '¡Solicitud enviada correctamente!', false);
    limpiarFormularioMatricula();
  } catch (err) {
    mostrarMensajeForm('matricula-msg', 'Ocurrió un error al enviar. Intenta nuevamente o escríbenos por WhatsApp.', true);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Enviar solicitud de matrícula 🎒';
  }
}

function limpiarFormularioMatricula() {
  ['mp-apoderado', 'mp-telefono', 'mp-alumno', 'mp-edad', 'mp-comentarios'].forEach(id => {
    document.getElementById(id).value = '';
  });
  document.getElementById('mp-nivel').value = '';
}


/* ============================================================
   FORMULARIO PÚBLICO: CONTACTO
   ============================================================ */
async function enviarContacto() {
  ocultarMensajeForm('contacto-msg');

  const faltantes = validarCampos({
    'ct-nombre': 'Nombre completo',
    'ct-telefono': 'Teléfono',
    'ct-motivo': 'Motivo de consulta',
    'ct-mensaje': 'Mensaje'
  });

  if (faltantes.length) {
    mostrarMensajeForm('contacto-msg', 'Por favor completa todos los campos obligatorios (*) antes de enviar.', true);
    document.getElementById('contacto-msg').scrollIntoView({ behavior: 'smooth', block: 'center' });
    return;
  }

  const payload = {
    nombre: document.getElementById('ct-nombre').value.trim(),
    telefono: document.getElementById('ct-telefono').value.trim(),
    motivo: document.getElementById('ct-motivo').value,
    mensaje: document.getElementById('ct-mensaje').value.trim(),
  };

  const btn = document.getElementById('ct-submit-btn');
  btn.disabled = true;
  btn.textContent = 'Enviando...';

  try {
    const res = await fetch('/api/contacto', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (!res.ok) {
      mostrarMensajeForm('contacto-msg', 'Faltan datos: ' + (data.campos || []).join(', '), true);
      return;
    }

    mostrarMensajeForm('contacto-msg', data.mensaje || '¡Mensaje enviado correctamente!', false);
    limpiarFormularioContacto();
  } catch (err) {
    mostrarMensajeForm('contacto-msg', 'Ocurrió un error al enviar. Intenta nuevamente o escríbenos por WhatsApp.', true);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Enviar mensaje ✉️';
  }
}

function limpiarFormularioContacto() {
  ['ct-nombre', 'ct-telefono', 'ct-mensaje'].forEach(id => {
    document.getElementById(id).value = '';
  });
  document.getElementById('ct-motivo').value = '';
}