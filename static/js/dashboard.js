/* ============================
   DATOS INICIALES (demo)
   ============================ */
let matriculas = [
  { id: 1, alumno: 'Ana García',    nivel: 'Inicial – 4 años',      apoderado: 'Rosa García',   telefono: '+51 945373930', estado: 'Confirmado' },
  { id: 2, alumno: 'Luis Pérez',    nivel: 'Primaria – 2° grado',   apoderado: 'Carlos Pérez',  telefono: '+51 912345678', estado: 'Pendiente'  },
  { id: 3, alumno: 'Sofía Torres',  nivel: 'Primaria – 5° grado',   apoderado: 'María Torres',  telefono: '+51 987654321', estado: 'En proceso' },
];

let alumnos = [
  { id: 1, nombre: 'Ana García',    grado: 'Inicial – 4 años',    edad: 4,  apoderado: 'Rosa García',   telefono: '+51 945373930' },
  { id: 2, nombre: 'Luis Pérez',    grado: 'Primaria – 2° grado', edad: 7,  apoderado: 'Carlos Pérez',  telefono: '+51 912345678' },
  { id: 3, nombre: 'Sofía Torres',  grado: 'Primaria – 5° grado', edad: 11, apoderado: 'María Torres',  telefono: '+51 987654321' },
  { id: 4, nombre: 'Diego Ramírez', grado: 'Primaria – 1° grado', edad: 6,  apoderado: 'Juan Ramírez',  telefono: '+51 934567890' },
];

let docentes = [
  { id: 1, nombre: 'Sra. Lucía Mendoza', especialidad: 'Comunicación', nivel: 'Primaria', telefono: '+51 911111111' },
  { id: 2, nombre: 'Sr. Marcos Quispe',  especialidad: 'Matemática',   nivel: 'Primaria', telefono: '+51 922222222' },
  { id: 3, nombre: 'Sra. Elena Vargas',  especialidad: 'Inicial',      nivel: 'Inicial',  telefono: '+51 933333333' },
];

let productos = [
  { id: 1, nombre: 'Comunicación – Nivel Inicial', cat: 'Libros',   precio: 35.00, stock: 20  },
  { id: 2, nombre: 'Matemática – Nivel Inicial',   cat: 'Libros',   precio: 32.00, stock: 15  },
  { id: 3, nombre: 'Polo Colegio',                 cat: 'Uniforme', precio: 28.00, stock: 50  },
  { id: 4, nombre: 'Buzo Completo',                cat: 'Uniforme', precio: 85.00, stock: 30  },
  { id: 5, nombre: 'Agenda Escolar',               cat: 'Agenda',   precio: 20.00, stock: 100 },
];

/* Contadores de ID para nuevos registros */
let nextId = { mat: 4, alu: 5, doc: 4, prod: 6 };


/* ============================
   HELPERS
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
}

/* Cerrar modal al hacer clic fuera */
document.querySelectorAll('.modal-bg').forEach(bg => {
  bg.addEventListener('click', function (e) {
    if (e.target === this) {
      this.classList.remove('open');
    }
  });
});


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

  /* Gráfico: Matrículas por nivel */
  const niveles  = ['Inicial', 'Primaria'];
  const colores  = ['#185FA5', '#0F6E56'];
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

  /* Gráfico: Productos por categoría */
  const cats    = ['Libros', 'Uniforme', 'Agenda', 'Útiles'];
  const colCat  = ['#185FA5', '#0F6E56', '#BA7517', '#993C1D'];
  const maxC    = Math.max(...cats.map(c => productos.filter(p => p.cat === c).length), 1);

  document.getElementById('chart-cats').innerHTML = cats.map((c, i) => {
    const cnt = productos.filter(p => p.cat === c).length;
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

  /* Tabla: últimas 3 matrículas */
  document.getElementById('dash-matriculas').innerHTML = matriculas.slice(-3).reverse().map(m => `
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
          <button class="btn btn-sm" title="Editar" onclick="editMat(${m.id})">
            <i class="ti ti-edit"></i>
          </button>
          <button class="btn btn-sm btn-danger" title="Eliminar" onclick="deleteMat(${m.id})">
            <i class="ti ti-trash"></i>
          </button>
        </div>
      </td>
    </tr>`).join('');
  updateDash();
}

function saveMat() {
  const editId = parseInt(document.getElementById('mat-edit-id').value);
  const obj = {
    id:         editId === -1 ? nextId.mat++ : editId,
    alumno:     document.getElementById('mat-alumno').value.trim()    || 'Sin nombre',
    nivel:      document.getElementById('mat-nivel').value,
    apoderado:  document.getElementById('mat-apoderado').value.trim() || '—',
    telefono:   document.getElementById('mat-telefono').value.trim()  || '—',
    estado:     document.getElementById('mat-estado').value,
  };

  if (editId === -1) {
    matriculas.push(obj);
  } else {
    const idx = matriculas.findIndex(m => m.id === editId);
    if (idx > -1) matriculas[idx] = obj;
  }

  closeModal('mat');
  renderMat();
  /* Resetear modal */
  document.getElementById('mat-edit-id').value = '-1';
  document.getElementById('mat-modal-title').textContent = 'Nueva matrícula';
  limpiarCampos(['mat-alumno', 'mat-apoderado', 'mat-telefono']);
}

function editMat(id) {
  const m = matriculas.find(x => x.id === id);
  if (!m) return;
  document.getElementById('mat-edit-id').value          = id;
  document.getElementById('mat-modal-title').textContent = 'Editar matrícula';
  document.getElementById('mat-alumno').value            = m.alumno;
  document.getElementById('mat-nivel').value             = m.nivel;
  document.getElementById('mat-apoderado').value         = m.apoderado;
  document.getElementById('mat-telefono').value          = m.telefono;
  document.getElementById('mat-estado').value            = m.estado;
  openModal('mat');
}

function deleteMat(id) {
  if (!confirm('¿Eliminar esta matrícula?')) return;
  matriculas = matriculas.filter(m => m.id !== id);
  renderMat();
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
          <button class="btn btn-sm" title="Editar" onclick="editAlu(${a.id})">
            <i class="ti ti-edit"></i>
          </button>
          <button class="btn btn-sm btn-danger" title="Eliminar" onclick="deleteAlu(${a.id})">
            <i class="ti ti-trash"></i>
          </button>
        </div>
      </td>
    </tr>`).join('');
  updateDash();
}

function saveAlu() {
  const editId = parseInt(document.getElementById('alu-edit-id').value);
  const obj = {
    id:        editId === -1 ? nextId.alu++ : editId,
    nombre:    document.getElementById('alu-nombre').value.trim()    || 'Sin nombre',
    grado:     document.getElementById('alu-grado').value,
    edad:      parseInt(document.getElementById('alu-edad').value)   || 0,
    apoderado: document.getElementById('alu-apoderado').value.trim() || '—',
    telefono:  document.getElementById('alu-telefono').value.trim()  || '—',
  };

  if (editId === -1) {
    alumnos.push(obj);
  } else {
    const idx = alumnos.findIndex(a => a.id === editId);
    if (idx > -1) alumnos[idx] = obj;
  }

  closeModal('alu');
  renderAlu();
  document.getElementById('alu-edit-id').value = '-1';
  document.getElementById('alu-modal-title').textContent = 'Nuevo alumno';
  limpiarCampos(['alu-nombre', 'alu-edad', 'alu-apoderado', 'alu-telefono']);
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
  openModal('alu');
}

function deleteAlu(id) {
  if (!confirm('¿Eliminar este alumno?')) return;
  alumnos = alumnos.filter(a => a.id !== id);
  renderAlu();
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
          <button class="btn btn-sm" title="Editar" onclick="editDoc(${d.id})">
            <i class="ti ti-edit"></i>
          </button>
          <button class="btn btn-sm btn-danger" title="Eliminar" onclick="deleteDoc(${d.id})">
            <i class="ti ti-trash"></i>
          </button>
        </div>
      </td>
    </tr>`).join('');
  updateDash();
}

function saveDoc() {
  const editId = parseInt(document.getElementById('doc-edit-id').value);
  const obj = {
    id:           editId === -1 ? nextId.doc++ : editId,
    nombre:       document.getElementById('doc-nombre').value.trim()       || 'Sin nombre',
    especialidad: document.getElementById('doc-especialidad').value.trim() || '—',
    nivel:        document.getElementById('doc-nivel').value,
    telefono:     document.getElementById('doc-telefono').value.trim()     || '—',
  };

  if (editId === -1) {
    docentes.push(obj);
  } else {
    const idx = docentes.findIndex(d => d.id === editId);
    if (idx > -1) docentes[idx] = obj;
  }

  closeModal('doc');
  renderDoc();
  document.getElementById('doc-edit-id').value = '-1';
  document.getElementById('doc-modal-title').textContent = 'Nuevo docente';
  limpiarCampos(['doc-nombre', 'doc-especialidad', 'doc-telefono']);
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
  openModal('doc');
}

function deleteDoc(id) {
  if (!confirm('¿Eliminar este docente?')) return;
  docentes = docentes.filter(d => d.id !== id);
  renderDoc();
}


/* ============================
   CRUD – TIENDA / PRODUCTOS
   ============================ */
function renderProd() {
  const tbody = document.getElementById('prod-tbody');
  tbody.innerHTML = productos.map(p => `
    <tr>
      <td>${p.nombre}</td>
      <td>${p.cat}</td>
      <td>S/ ${p.precio.toFixed(2)}</td>
      <td>${p.stock}</td>
      <td>
        <div class="acciones">
          <button class="btn btn-sm" title="Editar" onclick="editProd(${p.id})">
            <i class="ti ti-edit"></i>
          </button>
          <button class="btn btn-sm btn-danger" title="Eliminar" onclick="deleteProd(${p.id})">
            <i class="ti ti-trash"></i>
          </button>
        </div>
      </td>
    </tr>`).join('');
  updateDash();
}

function saveProd() {
  const editId = parseInt(document.getElementById('prod-edit-id').value);
  const obj = {
    id:     editId === -1 ? nextId.prod++ : editId,
    nombre: document.getElementById('prod-nombre').value.trim() || 'Sin nombre',
    cat:    document.getElementById('prod-cat').value,
    precio: parseFloat(document.getElementById('prod-precio').value) || 0,
    stock:  parseInt(document.getElementById('prod-stock').value)    || 0,
  };

  if (editId === -1) {
    productos.push(obj);
  } else {
    const idx = productos.findIndex(p => p.id === editId);
    if (idx > -1) productos[idx] = obj;
  }

  closeModal('prod');
  renderProd();
  document.getElementById('prod-edit-id').value = '-1';
  document.getElementById('prod-modal-title').textContent = 'Nuevo producto';
  limpiarCampos(['prod-nombre', 'prod-precio', 'prod-stock']);
}

function editProd(id) {
  const p = productos.find(x => x.id === id);
  if (!p) return;
  document.getElementById('prod-edit-id').value           = id;
  document.getElementById('prod-modal-title').textContent  = 'Editar producto';
  document.getElementById('prod-nombre').value             = p.nombre;
  document.getElementById('prod-cat').value                = p.cat;
  document.getElementById('prod-precio').value             = p.precio;
  document.getElementById('prod-stock').value              = p.stock;
  openModal('prod');
}

function deleteProd(id) {
  if (!confirm('¿Eliminar este producto?')) return;
  productos = productos.filter(p => p.id !== id);
  renderProd();
}


/* ============================
   INICIALIZAR
   ============================ */
renderMat();
renderAlu();
renderDoc();
renderProd();
