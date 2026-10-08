import re,sys,os
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 9box/
src=open(os.path.join(BASE,'index.html')).read()
logo=re.search(r'<svg [^>]*class="topbar-logo".*?</svg>',src,re.S).group(0)
bl=re.search(r'const BU_LEVEL=\{.*?\n\};',src,re.S).group(0)
meta=re.search(r'const BU_META=\[.*?\n\];',src,re.S).group(0)
period=re.search(r"const DATA_PERIOD='([^']*)'",src).group(1)
html=r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>9-Box · A &amp; C Focus · __PERIOD__ — Coteccons</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend+Deca:wght@300;400;500;600;700&display=swap');
:root{--navy:#16315E;--teal:#5FD1C1;--ink:#1C2B3A;--ink2:#42506B;--muted:#6B7A8D;--line:#D5DFEF;--bg:#F0F4FA;--card:#fff;
  --a:#51AC70;--a-ink:#2E7A4A;--a-bg:#EEF8F1;--c:#B86054;--c-ink:#8B3C30;--c-bg:#FDF1EE;
  --l4:#86b6ef;--l5:#5598e7;--l6:#2a78d6;--l7:#1c5cab;--l8:#104281;--lo:#D9DFE8}
*{box-sizing:border-box;margin:0;padding:0}
html,body{min-height:100vh;font-family:'Lexend Deca',sans-serif;background:var(--bg);color:var(--ink)}
.topbar{background:var(--navy);padding:0 32px;height:54px;display:flex;align-items:center;position:sticky;top:0;z-index:100;border-bottom:2.5px solid var(--teal)}
.topbar-left{display:flex;align-items:center;gap:14px;min-width:0}
.topbar-logo{height:26px;width:auto;flex-shrink:0;display:block}
.topbar-divider{width:1px;height:20px;background:rgba(255,255,255,.25);flex-shrink:0}
.subtitle{font-size:12px;font-weight:700;color:var(--teal);letter-spacing:.5px;white-space:nowrap}
.back-link{margin-left:auto;font-size:12px;font-weight:600;color:#fff;text-decoration:none;padding:6px 14px;border-radius:16px;border:1px solid rgba(255,255,255,.3);white-space:nowrap}
.back-link:hover{background:rgba(255,255,255,.14);border-color:rgba(255,255,255,.55)}
.page{padding:24px 32px;max-width:1440px;margin:0 auto}
.page-sub{font-size:13px;color:var(--ink2);margin-bottom:16px;padding-left:11px;border-left:3px solid var(--teal);line-height:1.45}
.section-label{display:flex;align-items:center;font-size:11.5px;font-weight:600;color:var(--muted);letter-spacing:.6px;text-transform:uppercase;margin:0 0 10px}
.step-n{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;background:var(--navy);color:#fff;font-size:11px;font-weight:700;margin-right:8px;flex-shrink:0}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px}
.bu-btn{padding:7px 18px;border-radius:20px;border:1px solid var(--line);background:#fff;color:var(--muted);font-size:12.5px;font-weight:500;cursor:pointer;transition:all .12s;font-family:inherit}
.bu-btn:hover{border-color:var(--navy);color:var(--navy)}
.bu-btn.sel{background:var(--navy);color:#fff;border-color:var(--navy)}
.scope-line{font-size:12px;color:var(--muted);margin-bottom:22px}
.scope-line strong{color:var(--ink)}
.zone-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-bottom:26px}
.bcard{background:var(--card);border:1px solid var(--line);border-radius:10px;box-shadow:0 1px 10px rgba(22,49,94,.055);overflow:hidden;display:flex;flex-direction:column}
.bcard-hdr{padding:14px 18px 10px;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;border-top:4px solid var(--zc)}
.bcard-key{font-size:22px;font-weight:700;color:var(--zink)}
.bcard-name{font-size:12.5px;font-weight:600;color:var(--ink)}
.bcard-n{width:100%;font-size:12px;color:var(--muted)}
.bcard-n strong{color:var(--ink);font-weight:700}
.action{margin:0 18px 6px;padding:9px 12px;border-radius:7px;background:var(--zbg);border:1px solid var(--zc);font-size:12px;line-height:1.45;color:var(--ink2)}
.action b{color:var(--zink);font-weight:700;margin-right:4px}
.bcard-body{display:flex;align-items:center;gap:16px;padding:12px 18px 18px;flex:1}
.pie-box{flex:0 0 auto;display:flex;align-items:center;justify-content:center}
.pie-box svg{display:block;overflow:visible}
.slice{cursor:pointer;transition:opacity .12s}
.pie-svg:hover .slice{opacity:.55}
.pie-svg:hover .slice:hover,.slice:focus{opacity:1;outline:none}
.slice-lbl{pointer-events:none;font-size:11px;font-weight:600}
.legend{flex:1;min-width:0;border-collapse:collapse;font-size:12px}
.legend td{padding:4px 4px;border-bottom:1px solid #EEF2F8;white-space:nowrap}
.legend td.num{text-align:right;font-variant-numeric:tabular-nums;color:var(--ink);font-weight:600}
.legend td.pct{text-align:right;font-variant-numeric:tabular-nums;color:var(--muted);width:44px}
.legend tr.lo td{color:var(--muted)} .legend tr.lo td.num{color:var(--muted);font-weight:500}
.legend tr.tot td{border-bottom:none;border-top:1.5px solid var(--line);font-weight:700;color:var(--ink)}
.legend tr.hl td{background:#F3F7FD}
.sw{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:7px;vertical-align:-1px}
.empty{font-size:12px;color:var(--muted);font-style:italic}
.note{font-size:11.5px;color:var(--muted);line-height:1.6;margin-top:-8px}
.tip{position:fixed;z-index:200;pointer-events:none;background:#fff;border:1px solid var(--line);border-radius:7px;box-shadow:0 4px 18px rgba(22,49,94,.16);padding:8px 11px;font-size:12px;line-height:1.5;color:var(--ink2);opacity:0;transition:opacity .1s;max-width:260px}
.tip .tv{font-size:15px;font-weight:700;color:var(--ink)}
.tip .tk{display:inline-block;width:12px;height:3px;border-radius:2px;margin-right:6px;vertical-align:3px}
.site-footer{margin-top:32px;padding:14px 32px;background:var(--bg);border-top:1px solid var(--line);display:flex;align-items:center;justify-content:center;gap:10px;font-size:11px;color:var(--muted);letter-spacing:.3px;flex-wrap:wrap}
.site-footer strong{color:var(--navy);font-weight:700}
.site-footer .ftr-dot{color:#C4CAD6}
.site-footer .ftr-warn{color:var(--navy);font-weight:600}
@media(max-width:1180px){.zone-row{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:760px){.page{padding:18px 16px}.topbar{padding:0 16px}.subtitle{display:none}.zone-row{grid-template-columns:1fr}.bcard-body{flex-direction:column;align-items:stretch}.legend{width:100%}}
</style>
</head>
<body>
<div class="topbar">
  <div class="topbar-left">
    __LOGO__
    <div class="topbar-divider"></div>
    <div class="subtitle">9-BOX · A &amp; C FOCUS · __PERIOD__</div>
  </div>
  <a class="back-link" href="index.html" title="Back to the full 9-Box dashboard">← Full 9-Box dashboard</a>
</div>

<div class="page">
  <div class="page-sub">Where do the top-talent (A) and needs-attention (C) boxes sit across senior levels L4–L8 — and what is the agreed action for each box?</div>

  <div class="section-label"><span class="step-n">1</span>Select business unit</div>
  <div class="filters" id="bu-filter" role="group" aria-label="Business unit filter"></div>
  <div class="scope-line" id="scope-line"></div>

  <div class="section-label"><span class="step-n">2</span>A-zone · talent pipeline</div>
  <div class="zone-row" id="row-a"></div>

  <div class="section-label"><span class="step-n">3</span>C-zone · performance risk</div>
  <div class="zone-row" id="row-c"></div>

  <div class="note">Pie area is proportional to headcount, on one shared scale across all six boxes in the current view. Slices L4–L8 are highlighted; L1–L3 are grouped in grey. Percentages in the legend are shares of the box; hover a slice for its share of the whole level.</div>
</div>

<div class="site-footer">
  <strong>Coteccons</strong><span class="ftr-dot">·</span><span class="ftr-warn">Internal / Confidential</span><span class="ftr-dot">·</span><span>By Human Capital</span>
</div>
<div class="tip" id="tip" role="tooltip"></div>

<script>
/* ═══ DATA — copied from index.html (same period). Re-run the build when index.html data changes. ═══ */
__BL__
__META__
/* ═══ CONFIG ═══ */
const BOXES={
  A1:{zone:'a',name:'High performance · High potential',tag:'Ready now',action:'Promotable at any point within the next 12 months.'},
  A2:{zone:'a',name:'Medium performance · High potential',tag:'Ready later',action:'Ready for the next role in 2–3 years.'},
  A3:{zone:'a',name:'High performance · Medium potential',tag:'Ready later',action:'Ready for the next role in 2–3 years.'},
  C1:{zone:'c',name:'Medium performance · Low potential',tag:'Improvement plan',action:'Needs a structured improvement plan.'},
  C2:{zone:'c',name:'Low performance · Medium potential',tag:'Improvement plan',action:'Needs a structured improvement plan.'},
  C3:{zone:'c',name:'Low performance · Low potential',tag:'PIP or manage out',action:'Performance improvement plan, or manage out.'},
};
/* slices in drawing order: L4..L8 highlighted, then L1–L3 grouped */
const SLICES=[
  {key:'L4',lv:[3],color:'var(--l4)',hex:'#86b6ef',txt:'#16315E'},
  {key:'L5',lv:[4],color:'var(--l5)',hex:'#5598e7',txt:'#fff'},
  {key:'L6',lv:[5],color:'var(--l6)',hex:'#2a78d6',txt:'#fff'},
  {key:'L7',lv:[6],color:'var(--l7)',hex:'#1c5cab',txt:'#fff'},
  {key:'L8',lv:[7],color:'var(--l8)',hex:'#104281',txt:'#fff'},
  {key:'L1–L3',lv:[0,1,2],color:'var(--lo)',hex:'#D9DFE8',txt:'#42506B',lo:true},
];
const R_MAX=92, R_MIN_LABEL=34, MIN_LABEL_ANGLE=0.42;
const UNITS=BU_META.map(b=>b.id);
let curBU='Overall';

const fmt=n=>n.toLocaleString('en-US');
const pct=(a,b)=>b?Math.round(a/b*100)+'%':'—';

function boxCounts(bu){
  const units=bu==='Overall'?UNITS:[bu];
  const out={}, lvTotal=Array(8).fill(0);
  Object.keys(BOXES).forEach(k=>out[k]=Array(8).fill(0));
  units.forEach(u=>{for(let i=0;i<8;i++){const row=BU_LEVEL[u][i];
    for(const k in row){lvTotal[i]+=row[k]; if(out[k]) out[k][i]+=row[k];}}});
  return {out,lvTotal};
}

function arcPath(cx,cy,r,a0,a1){
  if(a1-a0>=Math.PI*2-1e-6) return `M ${cx} ${cy-r} A ${r} ${r} 0 1 1 ${cx-0.01} ${cy-r} Z`;
  const x0=cx+r*Math.sin(a0),y0=cy-r*Math.cos(a0),x1=cx+r*Math.sin(a1),y1=cy-r*Math.cos(a1);
  return `M ${cx} ${cy} L ${x0} ${y0} A ${r} ${r} 0 ${a1-a0>Math.PI?1:0} 1 ${x1} ${y1} Z`;
}

function el(tag,attrs,parent){const ns=['svg','path','text','circle','g','title'].includes(tag)?'http://www.w3.org/2000/svg':null;
  const e=ns?document.createElementNS(ns,tag):document.createElement(tag);
  for(const a in attrs){if(a==='text')e.textContent=attrs[a];else e.setAttribute(a,attrs[a]);} if(parent)parent.appendChild(e);return e;}

const tip=document.getElementById('tip');
function showTip(ev,html){tip.innerHTML=html;tip.style.opacity=1;moveTip(ev);}
function moveTip(ev){const x=ev.clientX??(ev.target.getBoundingClientRect().right), y=ev.clientY??(ev.target.getBoundingClientRect().top);
  const w=tip.offsetWidth,h=tip.offsetHeight;let left=x+14,top=y+14;
  if(left+w>innerWidth-8)left=x-w-14; if(top+h>innerHeight-8)top=y-h-14; tip.style.left=left+'px';tip.style.top=top+'px';}
function hideTip(){tip.style.opacity=0;}

function renderCard(key,lv,lvTotal,rFor){
  const b=BOXES[key], total=lv.reduce((s,v)=>s+v,0), senior=lv.slice(3).reduce((s,v)=>s+v,0);
  const z=b.zone;
  const card=el('div',{class:'bcard',style:`--zc:var(--${z});--zink:var(--${z}-ink);--zbg:var(--${z}-bg)`});
  const hdr=el('div',{class:'bcard-hdr'},card);
  el('span',{class:'bcard-key',text:key},hdr); el('span',{class:'bcard-name',text:b.name},hdr);
  const n=el('div',{class:'bcard-n'},hdr);
  n.innerHTML=total?`<strong>${fmt(total)}</strong> employees · <strong>${fmt(senior)}</strong> at L4+ (${pct(senior,total)})`:'No employees in this view';
  const act=el('div',{class:'action'},card); el('b',{text:b.tag+' —'},act); act.appendChild(document.createTextNode(' '+b.action));
  const body=el('div',{class:'bcard-body'},card);
  const box=el('div',{class:'pie-box',style:`width:${R_MAX*2+4}px;height:${R_MAX*2+4}px`},body);
  const rows=SLICES.map(s=>({...s,n:s.lv.reduce((a,i)=>a+lv[i],0),lvN:s.lv.reduce((a,i)=>a+lvTotal[i],0)}));
  if(!total){ const svg=el('svg',{width:R_MAX*2+4,height:R_MAX*2+4,viewBox:`0 0 ${R_MAX*2+4} ${R_MAX*2+4}`,'aria-hidden':'true'},box);
    el('circle',{cx:R_MAX+2,cy:R_MAX+2,r:24,fill:'none',stroke:'#C7D4E6','stroke-dasharray':'4 4'},svg); }
  else{
    const r=rFor(total), c=R_MAX+2;
    const svg=el('svg',{class:'pie-svg',width:R_MAX*2+4,height:R_MAX*2+4,viewBox:`0 0 ${R_MAX*2+4} ${R_MAX*2+4}`,role:'img','aria-label':`${key}: ${total} employees, ${senior} at L4 and above`},box);
    let a=0;
    rows.forEach(s=>{ if(!s.n) return; const a1=a+s.n/total*Math.PI*2;
      const p=el('path',{class:'slice',d:arcPath(c,c,r,a,a1),fill:s.hex,stroke:'#fff','stroke-width':2,'stroke-linejoin':'round',tabindex:0,'aria-label':`${s.key}: ${s.n}`},svg);
      const tipHtml=`<div><span class="tk" style="background:${s.hex}"></span>${key} · ${s.key}</div><div class="tv">${fmt(s.n)} employee${s.n===1?'':'s'}</div><div>${pct(s.n,total)} of ${key}</div><div>${pct(s.n,s.lvN)} of all ${s.key} assessed (${fmt(s.lvN)})</div>`;
      p.addEventListener('pointerenter',e=>{showTip(e,tipHtml);hl(card,s.key,true)}); p.addEventListener('pointermove',moveTip);
      p.addEventListener('pointerleave',()=>{hideTip();hl(card,s.key,false)});
      p.addEventListener('focus',e=>{showTip(e,tipHtml);hl(card,s.key,true)}); p.addEventListener('blur',()=>{hideTip();hl(card,s.key,false)});
      const mid=(a+a1)/2;
      if(r>=R_MIN_LABEL && (a1-a)>=MIN_LABEL_ANGLE){ const lr=r*0.64;
        el('text',{class:'slice-lbl',x:c+lr*Math.sin(mid),y:c-lr*Math.cos(mid)+4,'text-anchor':'middle',fill:s.txt,text:pct(s.n,total)},svg); }
      a=a1; });
  }
  const tb=el('table',{class:'legend'},body); const tbody=el('tbody',{},tb);
  rows.forEach(s=>{ const tr=el('tr',{class:s.lo?'lo':'', 'data-k':s.key},tbody);
    const td=el('td',{},tr); el('span',{class:'sw',style:`background:${s.hex}`},td); td.appendChild(document.createTextNode(s.key));
    el('td',{class:'num',text:fmt(s.n)},tr); el('td',{class:'pct',text:total?pct(s.n,total):'—'},tr); });
  const tr=el('tr',{class:'tot'},tbody); el('td',{text:'Total'},tr); el('td',{class:'num',text:fmt(total)},tr); el('td',{class:'pct',text:total?'100%':'—'},tr);
  return card;
}
function hl(card,k,on){card.querySelectorAll('.legend tr').forEach(tr=>tr.classList.toggle('hl',on&&tr.dataset.k===k));}

function render(){
  const {out,lvTotal}=boxCounts(curBU);
  const totals=Object.fromEntries(Object.keys(out).map(k=>[k,out[k].reduce((s,v)=>s+v,0)]));
  const maxN=Math.max(1,...Object.values(totals));
  const rFor=n=>R_MAX*Math.sqrt(n/maxN);
  ['a','c'].forEach(z=>{const row=document.getElementById('row-'+z); row.innerHTML='';
    Object.keys(BOXES).filter(k=>BOXES[k].zone===z).forEach(k=>row.appendChild(renderCard(k,out[k],lvTotal,rFor)));});
  const assessed=lvTotal.reduce((s,v)=>s+v,0), senior=lvTotal.slice(3).reduce((s,v)=>s+v,0);
  const sum=(z,from)=>Object.keys(BOXES).filter(k=>BOXES[k].zone===z).reduce((s,k)=>s+out[k].slice(from).reduce((a,v)=>a+v,0),0);
  document.getElementById('scope-line').innerHTML=
    `<strong>${curBU==='Overall'?'Company-wide':curBU}</strong> · ${fmt(assessed)} assessed · ${fmt(senior)} at L4+ · `+
    `A-zone at L4+: <strong>${fmt(sum('a',3))}</strong> of ${fmt(sum('a',0))} · C-zone at L4+: <strong>${fmt(sum('c',3))}</strong> of ${fmt(sum('c',0))}`;
  document.querySelectorAll('.bu-btn').forEach(b=>{b.classList.toggle('sel',b.dataset.bu===curBU);b.setAttribute('aria-pressed',b.dataset.bu===curBU);});
}
const f=document.getElementById('bu-filter');
['Overall',...UNITS].forEach(u=>{const b=el('button',{class:'bu-btn','data-bu':u,type:'button',text:u==='Overall'?'Company-wide':u},f);
  b.addEventListener('click',()=>{curBU=u;render();});});
render();
</script>
</body>
</html>
'''
out=html.replace('__LOGO__',logo).replace('__BL__',bl).replace('__META__',meta).replace('__PERIOD__',period)
open(os.path.join(BASE,'focus.html'),'w').write(out)
print('ok',len(out))
