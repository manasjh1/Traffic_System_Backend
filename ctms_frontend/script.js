// config
const BASE = "http://127.0.0.1:8000/api";
const logsTableBody = document.querySelector("#logs-table tbody");
const totalEventsEl = document.getElementById("total-events");
const totalViolationsEl = document.getElementById("total-violations");
const todayEventsEl = document.getElementById("today-events");
const weeklyCtx = document.getElementById("weeklyChart").getContext("2d");

let weeklyChart = null;

// tabs
const tabDash = document.getElementById("tab-dashboard");
const tabLogs = document.getElementById("tab-logs");
const tabUpload = document.getElementById("tab-upload");
const pages = { dashboard: document.getElementById("dashboard"), logs: document.getElementById("logs"), upload: document.getElementById("upload") };

function show(page){
  Object.values(pages).forEach(p=>p.classList.add("hidden"));
  pages[page].classList.remove("hidden");
  document.querySelectorAll("nav button").forEach(b=>b.classList.remove("active"));
  if(page==="dashboard") tabDash.classList.add("active");
  if(page==="logs") tabLogs.classList.add("active");
  if(page==="upload") tabUpload.classList.add("active");
}
tabDash.onclick = ()=>show("dashboard");
tabLogs.onclick = ()=>show("logs");
tabUpload.onclick = ()=>show("upload");
document.getElementById("refresh").onclick = ()=>{ loadStats(); loadLogs(); };

// API helpers
async function apiGet(path){
  const res = await fetch(BASE + path);
  return await res.json();
}

async function apiPostDetect(file){
  const fd = new FormData();
  fd.append("file", file);
  const res = await fetch(BASE + "/detect/", { method:"POST", body:fd });
  return await res.json();
}

// load stats
async function loadStats(){
  try{
    const data = await apiGet("/stats/");
    totalEventsEl.textContent = data.total_events ?? 0;
    totalViolationsEl.textContent = data.total_violations ?? 0;
    todayEventsEl.textContent = data.today_events ?? 0;

    // build weekly chart
    const labels = data.weekly_chart_data.map(x=>x.date).reverse();
    const values = data.weekly_chart_data.map(x=>x.count).reverse();

    if(weeklyChart) weeklyChart.destroy();
    weeklyChart = new Chart(weeklyCtx, {
      type: "bar",
      data:{ labels, datasets:[{ label:"Events (last 7 days)", data:values, backgroundColor: "rgba(43,124,255,0.8)" }]},
      options:{ responsive:true, plugins:{legend:{display:false}}}
    });
  }catch(e){
    console.error(e);
  }
}

// load logs
async function loadLogs(filter=""){
  try{
    const data = await apiGet("/logs/?limit=200");
    let logs = data.logs || [];
    if(filter){
      const q = filter.toLowerCase();
      logs = logs.filter(r => (r.number_plate_uuid || "").toLowerCase().includes(q));
    }

    logsTableBody.innerHTML = "";
    logs.forEach((r,i)=>{
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${i+1}</td>
        <td>${r.number_plate_uuid ?? ""}</td>
        <td>${r.vehicle_type ?? ""}</td>
        <td>${r.violation_type ?? ""}</td>
        <td>${r.helmet_status ?? ""}</td>
        <td>${r.speed ?? 0}</td>
        <td>${r.created_at ?? ""}</td>
      `;
      logsTableBody.appendChild(tr);
    });
  }catch(e){
    console.error(e);
  }
}

// upload handling
document.getElementById("btn-upload").addEventListener("click", async ()=>{
  const f = document.getElementById("file-input").files[0];
  if(!f){ alert("Choose an image first"); return; }
  const resultBox = document.getElementById("upload-result");
  resultBox.classList.add("hidden");
  const res = await apiPostDetect(f);
  document.getElementById("result-json").textContent = JSON.stringify(res, null, 2);
  resultBox.classList.remove("hidden");
  // quick refresh logs & stats
  await loadLogs();
  await loadStats();
});

// filtering
document.getElementById("btn-filter").addEventListener("click", ()=>{
  const q = document.getElementById("filter-plate").value.trim();
  loadLogs(q);
});
document.getElementById("btn-clear-filter").addEventListener("click", ()=>{
  document.getElementById("filter-plate").value = "";
  loadLogs();
});

// initial load
loadStats();
loadLogs();
show("dashboard");
