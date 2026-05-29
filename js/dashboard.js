const ADMIN_UID = 'Bi68Kqd5jBPun5bIgXo0u5yTNmj2';

const firebaseConfig = {
  apiKey: "AIzaSyDyARd_4HXdx9gEOguMDvncPV17j7kum-s",
  authDomain: "church-registration-grace.firebaseapp.com",
  projectId: "church-registration-grace",
  storageBucket: "church-registration-grace.firebasestorage.app",
  messagingSenderId: "402796692999",
  appId: "1:402796692999:web:15f01064b41197c4c9cca2",
  measurementId: "G-L3CD5ZX957"
};
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();
const auth = firebase.auth();

let allMembers = [];
let allRegistrations = [];
let isLoggedIn = false;

document.getElementById('currentDate').textContent = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

var savedEmail = localStorage.getItem('adminEmail');
var rememberEmail = localStorage.getItem('rememberEmail');
if (savedEmail && rememberEmail !== 'false') {
  document.getElementById('loginEmail').value = savedEmail;
  document.getElementById('rememberEmail').checked = true;
} else {
  document.getElementById('rememberEmail').checked = false;
}

let authInitTimer = setTimeout(function() {
  window.location.href = 'index.html';
}, 2000);

let wasAdmin = false;

auth.onAuthStateChanged(function(user) {
  if (user && user.uid === ADMIN_UID) {
    wasAdmin = true;
    isLoggedIn = true;
    document.getElementById('adminBtn').textContent = 'Logout';
    document.getElementById('loginError').style.display = 'none';
    hideLoginModal();
    clearTimeout(authInitTimer);
    authInitTimer = null;
  } else if (user && user.uid !== ADMIN_UID) {
    auth.signOut();
    window.location.href = 'index.html';
  } else if (!wasAdmin) {
    isLoggedIn = false;
  } else {
    window.location.href = 'index.html';
  }
});

function showSection(section) {
  if (!isLoggedIn) { showLoginModal(); return; }
  document.querySelectorAll('.form-section').forEach(s => s.classList.remove('active'));
  document.getElementById('section-' + section).classList.add('active');
  document.querySelectorAll('.sidebar-item').forEach(i => i.classList.remove('active'));
  const activeItem = document.querySelector('[data-section="' + section + '"]');
  if (activeItem) activeItem.classList.add('active');
  
  if (section === 'dashboard') loadDashboard();
  if (section === 'members') loadMembers();
  if (section === 'events') loadEvents();
  if (section === 'pastoral') loadCare();
  if (section === 'communications') loadAnnouncements();
  if (section === 'programs') loadPrograms();
}

function showLoginModal() { document.getElementById('loginModal').classList.add('show'); }
function hideLoginModal() { document.getElementById('loginModal').classList.remove('show'); }

document.getElementById('loginForm').onsubmit = function(e) {
  e.preventDefault();
  const email = document.getElementById('loginEmail').value;
  const password = document.getElementById('loginPassword').value;
  const errorEl = document.getElementById('loginError');
  errorEl.style.display = 'none';

  if (document.getElementById('rememberEmail').checked) {
    localStorage.setItem('adminEmail', email);
    localStorage.setItem('rememberEmail', 'true');
  } else {
    localStorage.removeItem('adminEmail');
    localStorage.setItem('rememberEmail', 'false');
  }

  auth.signInWithEmailAndPassword(email, password)
    .then(function(userCred) {
      if (userCred.user.uid !== ADMIN_UID) {
        auth.signOut();
        errorEl.textContent = 'Access denied. You are not authorized as admin.';
        errorEl.style.display = 'block';
      }
    })
    .catch(function(err) {
      errorEl.textContent = err.message;
      errorEl.style.display = 'block';
    });
};

function handleAdminBtn() {
  if (isLoggedIn) {
    auth.signOut();
  } else {
    showLoginModal();
  }
}

async function loadDashboard() {
  try {
    const snapshot = await db.collection('registrations').get();
    allRegistrations = snapshot.docs.map(d => {
      const data = d.data();
      return {
        id: d.id,
        ...data,
        status: data.status || 'active'
      };
    });
    const members = allRegistrations.filter(r => r.status === 'active');
    const newRegs = allRegistrations.filter(r => r.status === 'new' || r.status === 'pending');

    document.getElementById('totalMembers').textContent = members.length;
    document.getElementById('newRegistrations').textContent = newRegs.length;

    document.getElementById('recentRegistrations').innerHTML = allRegistrations.slice(0, 5).map(r => 
      '<tr><td>' + (r.name || '-') + '</td><td>' + (r.phone || '-') + '</td><td>' + (r.department || r.registrationType || '-') + '</td><td>' + (r.createdAt ? new Date(r.createdAt).toLocaleDateString() : '-') + '</td><td><span class="status-badge ' + (r.status || 'active') + '">' + (r.status || 'active') + '</span></td></tr>'
    ).join('');

    const attendance = JSON.parse(localStorage.getItem('today_attendance') || '[]');
    const rate = members.length > 0 ? Math.round((attendance.length / members.length) * 100) : 0;
    document.getElementById('attendanceRate').textContent = rate + '%';
    document.getElementById('upcomingEvents').textContent = '5';
  } catch (e) {
    console.error('Dashboard load error:', e);
  }
}

async function loadMembers() {
  try {
    const snapshot = await db.collection('registrations').get();
    allMembers = snapshot.docs.map(d => {
      const data = d.data();
      return { id: d.id, ...data, status: data.status || 'active' };
    });
    renderMembers(allMembers);
  } catch (e) {
    console.error('Error loading members:', e);
    document.getElementById('membersTable').innerHTML = '<tr><td colspan="6" style="text-align:center;color:#e74c3c">Error loading members</td></tr>';
  }
}

function renderMembers(members) {
  document.getElementById('membersTable').innerHTML = members.map(m => 
    '<tr><td><input type="checkbox" class="attend-checkbox" data-phone="' + cleanPhone(m.phone) + '"> ' + (m.name || '-') + '</td><td>' + (m.phone || '-') + '</td><td>' + (m.department || '-') + '</td><td>' + (m.createdAt ? new Date(m.createdAt).toLocaleDateString() : '-') + '</td><td><span class="status-badge ' + (m.status || 'active') + '">' + (m.status || 'active') + '</span></td><td><button class="action-btn view">View</button><button class="action-btn edit">Edit</button></td></tr>'
  ).join('');
  
  let saveBtn = document.getElementById('saveAttendanceBtn');
  if (!saveBtn) {
    saveBtn = document.createElement('button');
    saveBtn.id = 'saveAttendanceBtn';
    saveBtn.className = 'btn-primary';
    saveBtn.style.marginTop = '15px';
    saveBtn.innerHTML = '<i class="fas fa-save"></i> Save Attendance';
    saveBtn.onclick = saveAttendance;
    document.getElementById('membersTable').parentElement.appendChild(saveBtn);
  }
}

function searchMembers() {
  const q = document.getElementById('memberSearch').value.toLowerCase();
  renderMembers(allMembers.filter(m => (m.name || '').toLowerCase().includes(q)));
}

function filterMembers() {
  const d = document.getElementById('departmentFilter').value;
  renderMembers(d ? allMembers.filter(m => m.department === d) : allMembers);
}

async function loadEvents() {
  document.getElementById('eventsGrid').innerHTML = `
    <div class="stat-card"><div class="stat-value">Sunday Service</div><div class="stat-label">Every Sunday 8:00 AM</div></div>
    <div class="stat-card"><div class="stat-value">Monday Kyoto</div><div class="stat-label">7:00-9:00 AM</div></div>
    <div class="stat-card"><div class="stat-value">Wed Glory</div><div class="stat-label">6:00-7:00 PM</div></div>
    <div class="stat-card"><div class="stat-value">Counseling</div><div class="stat-label">Tue/Thu 7AM-3PM</div></div>
    <div class="stat-card"><div class="stat-value">Friday Prayers</div><div class="stat-label">9PM-2AM</div></div>
  `;
}

let adminPrograms = [];

function showProgramModal(index) {
  document.getElementById('programModal').classList.add('show');
  if (index !== undefined && adminPrograms[index]) {
    document.getElementById('progIndex').value = index;
    document.getElementById('progIcon').value = adminPrograms[index].icon || '';
    document.getElementById('progTitle').value = adminPrograms[index].title || '';
    document.getElementById('progDate').value = adminPrograms[index].date || '';
    document.getElementById('progTime').value = adminPrograms[index].time || '';
    document.getElementById('progDesc').value = adminPrograms[index].description || '';
  } else {
    document.getElementById('programForm').reset();
    document.getElementById('progIndex').value = '';
  }
}

function hideProgramModal() {
  document.getElementById('programModal').classList.remove('show');
}

document.getElementById('programForm').onsubmit = function(e) {
  e.preventDefault();
  const index = document.getElementById('progIndex').value;
  const prog = {
    icon: document.getElementById('progIcon').value.trim(),
    title: document.getElementById('progTitle').value.trim(),
    date: document.getElementById('progDate').value.trim(),
    time: document.getElementById('progTime').value.trim(),
    description: document.getElementById('progDesc').value.trim()
  };
  if (index !== '') {
    adminPrograms[Number(index)] = prog;
  } else {
    adminPrograms.push(prog);
  }
  savePrograms();
  renderPrograms();
  hideProgramModal();
};

function renderPrograms() {
  document.getElementById('programsTable').innerHTML = adminPrograms.map((p, i) =>
    '<tr><td><i class="fas ' + (p.icon || 'fa-calendar') + '"></i></td><td>' + (p.title || '-') + '</td><td>' + (p.date || '-') + '</td><td>' + (p.time || '-') + '</td><td>' + (p.description || '-') + '</td><td><button class="action-btn edit" onclick="showProgramModal(' + i + ')">Edit</button><button class="action-btn delete" onclick="deleteProgram(' + i + ')">Delete</button></td></tr>'
  ).join('');
}

function deleteProgram(index) {
  if (confirm('Delete this program?')) {
    adminPrograms.splice(index, 1);
    savePrograms();
    renderPrograms();
  }
}

async function loadPrograms() {
  try {
    const snap = await db.collection('settings').doc('programs').get();
    if (snap.exists && snap.data().upcoming) {
      adminPrograms = snap.data().upcoming;
    }
  } catch (e) {
    console.warn('Could not load programs from Firestore:', e);
  }
  renderPrograms();
}

function savePrograms() {
  db.collection('settings').doc('programs').set({ upcoming: adminPrograms, updatedAt: new Date().toISOString() })
    .catch(e => console.warn('Save programs error:', e));
}

async function loadCare() {
  document.getElementById('careTable').innerHTML = '<tr><td colspan="4" style="text-align:center;color:#6c757d">No care requests</td></tr>';
}

function showCareModal() { alert('Pastoral care form coming soon'); }
async function loadAnnouncements() { document.getElementById('announcementsTable').innerHTML = ''; }
function showAnnouncementModal() { alert('Announcement form coming soon'); }
function showComTab(tab) {
  document.querySelectorAll('[id^="com-"]').forEach(t => t.style.display = 'none');
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById('com-' + tab).style.display = 'block';
  document.querySelector('[data-comtab="' + tab + '"]').classList.add('active');
}
function sendWhatsApp() { alert('WhatsApp integration coming soon'); }
function saveAttendance() {
  const checkboxes = document.querySelectorAll('.attend-checkbox:checked');
  const attendance = Array.from(checkboxes).map(cb => cb.dataset.phone);
  localStorage.setItem('today_attendance', JSON.stringify(attendance));
  alert('Attendance saved! (' + attendance.length + ' present)');
}

function cleanPhone(phone) {
  return String(phone || '').replace(/\D/g, '').slice(-9);
}

document.querySelectorAll('.sidebar-item[data-section]').forEach(item => {
  item.addEventListener('click', () => {
    if (!isLoggedIn) {
      showLoginModal();
      return;
    }
    showSection(item.dataset.section);
  });
});

if (auth.currentUser) {
  loadDashboard();
}
