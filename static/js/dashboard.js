/* ============================================================
   DASHBOARD — conectado a la API real (Flask + SQLite)
   Los datos ya NO se guardan solo en memoria: cada acción
   (crear, editar, eliminar) llama al backend y persiste.
   ============================================================ */

let matriculas = [];
let alumnos = [];
let docentes = [];
let productos = [];

const API = "/api";

/* ============================
   UTILIDADES
   ============================ */
function estadoBadge(estado) {
  if (estado === 'Confirmado') return 'badge-green';
  if (estado === 'Pendiente')  return 'badge-amber';
  return 'badge-blue';
}

function limpiarCampos(ids) {
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
}

function showToast(mensaje, esError = false) {
  let toast = document.getElementById('app-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'app-toast';
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = mensaje;
  toast.classList.toggle('error', esError);
  toast.classList.add('show');
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove('show'), 3200);
}

// Solo letras (con tildes/ñ), espacios, apóstrofes y guiones.
const NOMBRE_REGEX = /^[A-Za-zÁÉÍÓÚÀÈÌÒÙÑÜáéíóúàèìòùñü'.\s-]{2,60}$/;

function nombreValido(valor) {
  return NOMBRE_REGEX.test((valor || '').trim());
}

function telefonoValido(valor) {
  let digitos = (valor || '').replace(/\D/g, '');
  if (digitos.startsWith('51') && digitos.length === 11) digitos = digitos.slice(2);
  return /^9\d{8}$/.test(digitos);
}

/* Valida un conjunto de campos.
   Formato: { idCampo: { label: 'Etiqueta', tipo: 'texto'|'nombre'|'telefono' } }
   (también acepta el formato viejo { idCampo: 'Etiqueta' } como tipo 'texto')
   Marca en rojo los inválidos/vacíos y devuelve la lista de etiquetas con problema. */
function validarCampos(mapaCampos) {
  const faltantes = [];
  Object.entries(mapaCampos).forEach(([id, config]) => {
    const cfg = typeof config === 'string' ? { label: config, tipo: 'texto' } : config;
    const el = document.getElementById(id);
    if (!el) return;
    const valor = (el.value || '').toString().trim();

    if (valor === '') {
      el.classList.add('input-error');
      faltantes.push(cfg.label);
      return;
    }
    if (cfg.tipo === 'nombre' && !nombreValido(valor)) {
      el.classList.add('input-error');
      faltantes.push(cfg.label + ' (solo letras y espacios)');
      return;
    }
    if (cfg.tipo === 'telefono' && !telefonoValido(valor)) {
      el.classList.add('input-error');
      faltantes.push(cfg.label + ' (debe tener 9 dígitos, ej: 945373930)');
      return;
    }
    el.classList.remove('input-error');
  });
  return faltantes;
}

function mostrarErrorModal(tipo, mensaje) {
  const box = document.getElementById(tipo + '-form-error');
  if (!box) return;
  box.textContent = mensaje;
  box.classList.add('show');
}

function limpiarErrorModal(tipo) {
  const box = document.getElementById(tipo + '-form-error');
  if (box) { box.textContent = ''; box.classList.remove('show'); }
  document.querySelectorAll(`#modal-${tipo} .input-error`).forEach(el => el.classList.remove('input-error'));
}

async function apiFetch(url, options = {}) {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  });
  let data = null;
  try { data = await res.json(); } catch (e) { /* sin cuerpo */ }
  return { ok: res.ok, status: res.status, data };
}


/* ============================
   NAVEGACIÓN ENTRE PÁGINAS
   ============================ */
function showPage(name, el) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('page-' + name).classList.add('active');
  el.classList.add('active');
}


/* ============================
   MODALS
   ============================ */
function openModal(type) {
  document.getElementById('modal-' + type).classList.add('open');
}

function closeModal(type) {
  document.getElementById('modal-' + type).classList.remove('open');
  limpiarErrorModal(type);
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.modal-bg').forEach(bg => {
    bg.addEventListener('click', function (e) {
      if (e.target === this) this.classList.remove('open');
    });
  });
});

/* Abrir modal en modo "nuevo" para cada tipo */
function abrirNuevaMat() {
  document.getElementById('mat-edit-id').value = -1;
  document.getElementById('mat-modal-title').textContent = 'Nueva matrícula';
  limpiarCampos(['mat-alumno', 'mat-edad', 'mat-apoderado', 'mat-telefono', 'mat-comentarios']);
  document.getElementById('mat-nivel').value = '';
  document.getElementById('mat-estado').value = 'Pendiente';
  limpiarErrorModal('mat');
  openModal('mat');
}
function abrirNuevoAlu() {
  document.getElementById('alu-edit-id').value = -1;
  document.getElementById('alu-modal-title').textContent = 'Nuevo alumno';
  limpiarCampos(['alu-nombre', 'alu-edad', 'alu-apoderado', 'alu-telefono']);
  document.getElementById('alu-grado').value = '';
  limpiarErrorModal('alu');
  openModal('alu');
}
function abrirNuevoDoc() {
  document.getElementById('doc-edit-id').value = -1;
  document.getElementById('doc-modal-title').textContent = 'Nuevo docente';
  limpiarCampos(['doc-nombre', 'doc-especialidad', 'doc-telefono']);
  limpiarErrorModal('doc');
  openModal('doc');
}
function abrirNuevoProd() {
  document.getElementById('prod-edit-id').value = -1;
  document.getElementById('prod-modal-title').textContent = 'Nuevo producto';
  limpiarCampos(['prod-nombre', 'prod-precio', 'prod-stock']);
  limpiarErrorModal('prod');
  openModal('prod');
}


/* ============================
   BÚSQUEDA / FILTRO DE TABLA
   ============================ */
function filterTable(tbodyId, query, cols) {
  const q = query.toLowerCase().trim();
  const rows = document.getElementById(tbodyId).querySelectorAll('tr');
  rows.forEach(row => {
    const cells = row.querySelectorAll('td');
    const match = q === '' || cols.some(i => cells[i] && cells[i].textContent.toLowerCase().includes(q));
    row.style.display = match ? '' : 'none';
  });
}


/* ============================
   DASHBOARD – ACTUALIZAR
   ============================ */
function updateDash() {
  document.getElementById('m-total').textContent    = matriculas.length;
  document.getElementById('m-alumnos').textContent  = alumnos.length;
  document.getElementById('m-docentes').textContent = docentes.length;
  document.getElementById('m-productos').textContent = productos.length;

  const niveles  = ['Inicial', 'Primaria'];
  const colores  = ['#F0955C', '#4A90C2'];
  const maxN     = Math.max(...niveles.map(n => matriculas.filter(m => m.nivel.startsWith(n)).length), 1);

  document.getElementById('chart-niveles').innerHTML = niveles.map((n, i) => {
    const cnt = matriculas.filter(m => m.nivel.startsWith(n)).length;
    const pct = Math.round((cnt / maxN) * 100);
    return `
      <div class="bar-row">
        <div class="bar-label">${n}</div>
        <div class="bar-track">
          <div class="bar-fill" style="width:${pct}%; background:${colores[i]}"></div>
        </div>
        <div class="bar-val">${cnt}</div>
      </div>`;
  }).join('');

  const cats    = ['Libros', 'Uniforme', 'Agenda', 'Útiles'];
  const colCat  = ['#4A90C2', '#5FB88F', '#F2BB4E', '#A67FC4'];
  const maxC    = Math.max(...cats.map(c => productos.filter(p => p.categoria === c).length), 1);

  document.getElementById('chart-cats').innerHTML = cats.map((c, i) => {
    const cnt = productos.filter(p => p.categoria === c).length;
    const pct = Math.round((cnt / maxC) * 100);
    return `
      <div class="bar-row">
        <div class="bar-label">${c}</div>
        <div class="bar-track">
          <div class="bar-fill" style="width:${pct}%; background:${colCat[i]}"></div>
        </div>
        <div class="bar-val">${cnt}</div>
      </div>`;
  }).join('');

  document.getElementById('dash-matriculas').innerHTML = matriculas.slice(0, 3).map(m => `
    <tr>
      <td>${m.alumno}</td>
      <td>${m.nivel}</td>
      <td>${m.apoderado}</td>
      <td><span class="badge ${estadoBadge(m.estado)}">${m.estado}</span></td>
    </tr>`).join('');
}


/* ============================
   CRUD – MATRÍCULAS
   ============================ */
function renderMat() {
  const tbody = document.getElementById('mat-tbody');
  tbody.innerHTML = matriculas.map(m => `
    <tr>
      <td>${m.alumno}</td>
      <td>${m.nivel}</td>
      <td>${m.apoderado}</td>
      <td>${m.telefono}</td>
      <td><span class="badge ${estadoBadge(m.estado)}">${m.estado}</span></td>
      <td>
        <div class="acciones">
          <button class="btn btn-sm" title="Editar" onclick="editMat(${m.id})"><i class="ti ti-edit"></i></button>
          <button class="btn btn-sm btn-danger" title="Eliminar" onclick="deleteMat(${m.id})"><i class="ti ti-trash"></i></button>
        </div>
      </td>
    </tr>`).join('');
  updateDash();
}

async function cargarMatriculas() {
  const { ok, data } = await apiFetch(`${API}/matriculas`);
  if (ok) { matriculas = data; renderMat(); }
}

async function saveMat() {
  limpiarErrorModal('mat');
  const faltantes = validarCampos({
    'mat-alumno': { label: 'Nombre del alumno', tipo: 'nombre' },
    'mat-edad': { label: 'Edad', tipo: 'texto' },
    'mat-nivel': { label: 'Nivel', tipo: 'texto' },
    'mat-apoderado': { label: 'Apoderado', tipo: 'nombre' },
    'mat-telefono': { label: 'Teléfono', tipo: 'telefono' },
    'mat-estado': { label: 'Estado', tipo: 'texto' }
  });
  if (faltantes.length) {
    mostrarErrorModal('mat', 'Completa estos campos obligatorios: ' + faltantes.join(', '));
    return;
  }

  const editId = parseInt(document.getElementById('mat-edit-id').value);
  const payload = {
    alumno: document.getElementById('mat-alumno').value.trim(),
    edad: parseInt(document.getElementById('mat-edad').value),
    nivel: document.getElementById('mat-nivel').value,
    apoderado: document.getElementById('mat-apoderado').value.trim(),
    telefono: document.getElementById('mat-telefono').value.trim(),
    comentarios: document.getElementById('mat-comentarios').value.trim(),
    estado: document.getElementById('mat-estado').value,
  };

  const url = editId === -1 ? `${API}/matriculas` : `${API}/matriculas/${editId}`;
  const method = editId === -1 ? 'POST' : 'PUT';
  const { ok, data } = await apiFetch(url, { method, body: JSON.stringify(payload) });

  if (!ok) {
    mostrarErrorModal('mat', data && data.error ? data.error + ': ' + (data.campos || []).join(', ') : 'No se pudo guardar.');
    return;
  }

  closeModal('mat');
  await cargarMatriculas();
  showToast(editId === -1 ? 'Matrícula creada correctamente' : 'Matrícula actualizada');
}

function editMat(id) {
  const m = matriculas.find(x => x.id === id);
  if (!m) return;
  document.getElementById('mat-edit-id').value          = id;
  document.getElementById('mat-modal-title').textContent = 'Editar matrícula';
  document.getElementById('mat-alumno').value            = m.alumno;
  document.getElementById('mat-edad').value               = m.edad || '';
  document.getElementById('mat-nivel').value              = m.nivel;
  document.getElementById('mat-apoderado').value          = m.apoderado;
  document.getElementById('mat-telefono').value           = m.telefono;
  document.getElementById('mat-comentarios').value        = m.comentarios || '';
  document.getElementById('mat-estado').value             = m.estado;
  limpiarErrorModal('mat');
  openModal('mat');
}

async function deleteMat(id) {
  if (!confirm('¿Eliminar esta matrícula?')) return;
  const { ok } = await apiFetch(`${API}/matriculas/${id}`, { method: 'DELETE' });
  if (ok) { await cargarMatriculas(); showToast('Matrícula eliminada'); }
  else showToast('No se pudo eliminar', true);
}


/* ============================
   CRUD – ALUMNOS
   ============================ */
function renderAlu() {
  const tbody = document.getElementById('alu-tbody');
  tbody.innerHTML = alumnos.map(a => `
    <tr>
      <td>${a.nombre}</td>
      <td>${a.grado}</td>
      <td>${a.edad} años</td>
      <td>${a.apoderado}</td>
      <td>${a.telefono}</td>
      <td>
        <div class="acciones">
          <button class="btn btn-sm" title="Editar" onclick="editAlu(${a.id})"><i class="ti ti-edit"></i></button>
          <button class="btn btn-sm btn-danger" title="Eliminar" onclick="deleteAlu(${a.id})"><i class="ti ti-trash"></i></button>
        </div>
      </td>
    </tr>`).join('');
  updateDash();
}

async function cargarAlumnos() {
  const { ok, data } = await apiFetch(`${API}/alumnos`);
  if (ok) { alumnos = data; renderAlu(); }
}

async function saveAlu() {
  limpiarErrorModal('alu');
  const faltantes = validarCampos({
    'alu-nombre': { label: 'Nombre', tipo: 'nombre' },
    'alu-grado': { label: 'Grado', tipo: 'texto' },
    'alu-edad': { label: 'Edad', tipo: 'texto' },
    'alu-apoderado': { label: 'Apoderado', tipo: 'nombre' },
    'alu-telefono': { label: 'Teléfono', tipo: 'telefono' }
  });
  if (faltantes.length) {
    mostrarErrorModal('alu', 'Completa estos campos obligatorios: ' + faltantes.join(', '));
    return;
  }

  const editId = parseInt(document.getElementById('alu-edit-id').value);
  const payload = {
    nombre: document.getElementById('alu-nombre').value.trim(),
    grado: document.getElementById('alu-grado').value,
    edad: parseInt(document.getElementById('alu-edad').value),
    apoderado: document.getElementById('alu-apoderado').value.trim(),
    telefono: document.getElementById('alu-telefono').value.trim(),
  };

  const url = editId === -1 ? `${API}/alumnos` : `${API}/alumnos/${editId}`;
  const method = editId === -1 ? 'POST' : 'PUT';
  const { ok, data } = await apiFetch(url, { method, body: JSON.stringify(payload) });

  if (!ok) {
    mostrarErrorModal('alu', data && data.error ? data.error + ': ' + (data.campos || []).join(', ') : 'No se pudo guardar.');
    return;
  }

  closeModal('alu');
  await cargarAlumnos();
  showToast(editId === -1 ? 'Alumno agregado correctamente' : 'Alumno actualizado');
}

function editAlu(id) {
  const a = alumnos.find(x => x.id === id);
  if (!a) return;
  document.getElementById('alu-edit-id').value           = id;
  document.getElementById('alu-modal-title').textContent  = 'Editar alumno';
  document.getElementById('alu-nombre').value             = a.nombre;
  document.getElementById('alu-grado').value              = a.grado;
  document.getElementById('alu-edad').value               = a.edad;
  document.getElementById('alu-apoderado').value          = a.apoderado;
  document.getElementById('alu-telefono').value           = a.telefono;
  limpiarErrorModal('alu');
  openModal('alu');
}

async function deleteAlu(id) {
  if (!confirm('¿Eliminar este alumno?')) return;
  const { ok } = await apiFetch(`${API}/alumnos/${id}`, { method: 'DELETE' });
  if (ok) { await cargarAlumnos(); showToast('Alumno eliminado'); }
  else showToast('No se pudo eliminar', true);
}


/* ============================
   CRUD – DOCENTES
   ============================ */
function renderDoc() {
  const tbody = document.getElementById('doc-tbody');
  tbody.innerHTML = docentes.map(d => `
    <tr>
      <td>${d.nombre}</td>
      <td>${d.especialidad}</td>
      <td>${d.nivel}</td>
      <td>${d.telefono}</td>
      <td>
        <div class="acciones">
          <button class="btn btn-sm" title="Editar" onclick="editDoc(${d.id})"><i class="ti ti-edit"></i></button>
          <button class="btn btn-sm btn-danger" title="Eliminar" onclick="deleteDoc(${d.id})"><i class="ti ti-trash"></i></button>
        </div>
      </td>
    </tr>`).join('');
  updateDash();
}

async function cargarDocentes() {
  const { ok, data } = await apiFetch(`${API}/docentes`);
  if (ok) { docentes = data; renderDoc(); }
}

async function saveDoc() {
  limpiarErrorModal('doc');
  const faltantes = validarCampos({
    'doc-nombre': { label: 'Nombre', tipo: 'nombre' },
    'doc-especialidad': { label: 'Especialidad', tipo: 'nombre' },
    'doc-nivel': { label: 'Nivel', tipo: 'texto' },
    'doc-telefono': { label: 'Teléfono', tipo: 'telefono' }
  });
  if (faltantes.length) {
    mostrarErrorModal('doc', 'Completa estos campos obligatorios: ' + faltantes.join(', '));
    return;
  }

  const editId = parseInt(document.getElementById('doc-edit-id').value);
  const payload = {
    nombre: document.getElementById('doc-nombre').value.trim(),
    especialidad: document.getElementById('doc-especialidad').value.trim(),
    nivel: document.getElementById('doc-nivel').value,
    telefono: document.getElementById('doc-telefono').value.trim(),
  };

  const url = editId === -1 ? `${API}/docentes` : `${API}/docentes/${editId}`;
  const method = editId === -1 ? 'POST' : 'PUT';
  const { ok, data } = await apiFetch(url, { method, body: JSON.stringify(payload) });

  if (!ok) {
    mostrarErrorModal('doc', data && data.error ? data.error + ': ' + (data.campos || []).join(', ') : 'No se pudo guardar.');
    return;
  }

  closeModal('doc');
  await cargarDocentes();
  showToast(editId === -1 ? 'Docente agregado correctamente' : 'Docente actualizado');
}

function editDoc(id) {
  const d = docentes.find(x => x.id === id);
  if (!d) return;
  document.getElementById('doc-edit-id').value           = id;
  document.getElementById('doc-modal-title').textContent  = 'Editar docente';
  document.getElementById('doc-nombre').value             = d.nombre;
  document.getElementById('doc-especialidad').value       = d.especialidad;
  document.getElementById('doc-nivel').value              = d.nivel;
  document.getElementById('doc-telefono').value           = d.telefono;
  limpiarErrorModal('doc');
  openModal('doc');
}

async function deleteDoc(id) {
  if (!confirm('¿Eliminar este docente?')) return;
  const { ok } = await apiFetch(`${API}/docentes/${id}`, { method: 'DELETE' });
  if (ok) { await cargarDocentes(); showToast('Docente eliminado'); }
  else showToast('No se pudo eliminar', true);
}


/* ============================
   CRUD – TIENDA / PRODUCTOS
   ============================ */
function renderProd() {
  const tbody = document.getElementById('prod-tbody');
  tbody.innerHTML = productos.map(p => `
    <tr>
      <td>${p.nombre}</td>
      <td>${p.categoria}</td>
      <td>S/ ${Number(p.precio).toFixed(2)}</td>
      <td>${p.stock}</td>
      <td>
        <div class="acciones">
          <button class="btn btn-sm" title="Editar" onclick="editProd(${p.id})"><i class="ti ti-edit"></i></button>
          <button class="btn btn-sm btn-danger" title="Eliminar" onclick="deleteProd(${p.id})"><i class="ti ti-trash"></i></button>
        </div>
      </td>
    </tr>`).join('');
  updateDash();
}

async function cargarProductos() {
  const { ok, data } = await apiFetch(`${API}/productos`);
  if (ok) { productos = data; renderProd(); }
}

async function saveProd() {
  limpiarErrorModal('prod');
  const faltantes = validarCampos({
    'prod-nombre': 'Nombre',
    'prod-cat': 'Categoría',
    'prod-precio': 'Precio',
    'prod-stock': 'Stock'
  });
  if (faltantes.length) {
    mostrarErrorModal('prod', 'Completa estos campos obligatorios: ' + faltantes.join(', '));
    return;
  }

  const editId = parseInt(document.getElementById('prod-edit-id').value);
  const payload = {
    nombre: document.getElementById('prod-nombre').value.trim(),
    categoria: document.getElementById('prod-cat').value,
    precio: parseFloat(document.getElementById('prod-precio').value),
    stock: parseInt(document.getElementById('prod-stock').value),
  };

  const url = editId === -1 ? `${API}/productos` : `${API}/productos/${editId}`;
  const method = editId === -1 ? 'POST' : 'PUT';
  const { ok, data } = await apiFetch(url, { method, body: JSON.stringify(payload) });

  if (!ok) {
    mostrarErrorModal('prod', data && data.error ? data.error + ': ' + (data.campos || []).join(', ') : 'No se pudo guardar.');
    return;
  }

  closeModal('prod');
  await cargarProductos();
  showToast(editId === -1 ? 'Producto agregado correctamente' : 'Producto actualizado');
}

function editProd(id) {
  const p = productos.find(x => x.id === id);
  if (!p) return;
  document.getElementById('prod-edit-id').value           = id;
  document.getElementById('prod-modal-title').textContent  = 'Editar producto';
  document.getElementById('prod-nombre').value             = p.nombre;
  document.getElementById('prod-cat').value                = p.categoria;
  document.getElementById('prod-precio').value             = p.precio;
  document.getElementById('prod-stock').value              = p.stock;
  limpiarErrorModal('prod');
  openModal('prod');
}

async function deleteProd(id) {
  if (!confirm('¿Eliminar este producto?')) return;
  const { ok } = await apiFetch(`${API}/productos/${id}`, { method: 'DELETE' });
  if (ok) { await cargarProductos(); showToast('Producto eliminado'); }
  else showToast('No se pudo eliminar', true);
}


/* ============================
   INICIALIZAR — carga todo desde la base de datos real
   ============================ */
(async function init() {
  await Promise.all([cargarMatriculas(), cargarAlumnos(), cargarDocentes(), cargarProductos()]);
})();