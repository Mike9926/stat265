import React, {useEffect, useState} from 'react'

function SmallSpark({data}){
  // very small inline sparkline using SVG
  if(!data || data.length===0) return <div style={{width:120,height:36}} />
  const max = Math.max(...data)
  const min = Math.min(...data)
  const points = data.map((v,i)=>{
    const x = (i/(data.length-1))*120
    const y = 36 - ((v-min)/(max-min||1))*36
    return `${x},${y}`
  }).join(' ')
  return (
    <svg width={120} height={36} viewBox={`0 0 120 36`}>
      <polyline fill="none" stroke="#2dd4bf" strokeWidth={1.5} points={points} />
    </svg>
  )
}

export default function Home(){
  const [summary,setSummary] = useState(null)
  useEffect(()=>{
    fetch('/api/market-summary/').then(r=>r.json()).then(setSummary).catch(()=>{})
  },[])

  const indexValue = summary ? summary.value.toLocaleString() : '—'
  const change = summary ? summary.change_percent : 0

  return (
    <div style={{background:'#07172a',minHeight:'100vh',color:'#e6eef7'}}>
      <header style={{padding:'1rem 2rem',display:'flex',alignItems:'center',justifyContent:'space-between',borderBottom:'1px solid rgba(255,255,255,0.03)'}}>
        <div style={{display:'flex',alignItems:'center',gap:12}}>
          <div style={{width:36,height:36,background:'#0ea5e9',borderRadius:6,display:'flex',alignItems:'center',justifyContent:'center',fontWeight:700}}>Z</div>
          <nav style={{display:'flex',gap:16,alignItems:'center'}}>
            <a href="#" style={{color:'#dbeafe',textDecoration:'none'}}>Home</a>
            <a href="#" style={{color:'#9fb3c9',textDecoration:'none'}}>About us</a>
            <a href="#" style={{color:'#9fb3c9',textDecoration:'none'}}>Services</a>
            <a href="#" style={{color:'#9fb3c9',textDecoration:'none'}}>Market Data</a>
          </nav>
        </div>
        <div>
          <button style={{background:'#1e40af',color:'#fff',padding:'8px 14px',borderRadius:8,border:'none'}}>Start Your Portfolio</button>
        </div>
      </header>

      <main style={{maxWidth:1100,margin:'2rem auto',padding:'0 1rem'}}>
        <section style={{display:'grid',gridTemplateColumns:'1fr 380px',gap:20,alignItems:'start'}}>
          <div>
            <h1 style={{fontSize:40,margin:0,lineHeight:1.05}}>Unlock Malawi's Financial Future. Seamlessly.</h1>
            <p style={{color:'#9fb3c9'}}>A digital-first platform for local and international investors — track, manage, and grow wealth with confidence.</p>
            <div style={{display:'flex',gap:12,marginTop:18}}>
              <button style={{background:'#0ea5e9',color:'#042c45',padding:'10px 16px',borderRadius:8,border:'none'}}>Explore the MSE (Guest View)</button>
              <button style={{background:'transparent',color:'#cfe8ff',padding:'10px 16px',borderRadius:8,border:'1px solid rgba(255,255,255,0.06)'}}>Start Your Portfolio</button>
            </div>
            <div style={{display:'flex',gap:12,marginTop:24}}>
              <div style={{flex:1,background:'#07233a',padding:14,borderRadius:10}}>
                <strong>Seamless</strong>
                <div style={{color:'#9fb3c9',fontSize:13}}>Portfolio Management</div>
              </div>
              <div style={{flex:1,background:'#07233a',padding:14,borderRadius:10}}>
                <strong>Live Market Insights</strong>
                <div style={{color:'#9fb3c9',fontSize:13}}>Real-time tickers</div>
              </div>
              <div style={{flex:1,background:'#07233a',padding:14,borderRadius:10}}>
                <strong>Invest Globally</strong>
                <div style={{color:'#9fb3c9',fontSize:13}}>Access global markets</div>
              </div>
            </div>
          </div>

          <aside style={{background:'#041426',padding:18,borderRadius:12}}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
              <div>
                <div style={{color:'#9fb3c9',fontSize:12}}>MSE</div>
                <div style={{fontSize:28,fontWeight:700}}>{indexValue}</div>
                <div style={{color: change>=0 ? '#10b981':'#ef4444'}}>{change>=0?`+${change}%`:`${change}%`}</div>
              </div>
              <div>
                <SmallSpark data={[1,2,3,2.5,3.2,4,4.2,4.5].map(n=>n+ (summary? (summary.value%5):0))} />
              </div>
            </div>

            <div style={{marginTop:16}}>
              <div style={{display:'flex',justifyContent:'space-between',marginBottom:8}}>
                <strong style={{color:'#cfe8ff'}}>Top Gainers</strong>
                <a href="#" style={{color:'#7dd3fc',fontSize:13}}>See all</a>
              </div>
              <div>
                {(summary && summary.gainers.length>0) ? summary.gainers.map((g)=> (
                  <div key={g.symbol} style={{display:'flex',justifyContent:'space-between',padding:'8px 0',borderBottom:'1px solid rgba(255,255,255,0.02)'}}>
                    <div>
                      <div style={{fontWeight:600}}>{g.symbol}</div>
                      <div style={{fontSize:12,color:'#9fb3c9'}}>MSE</div>
                    </div>
                    <div style={{textAlign:'right'}}>
                      <div style={{color:'#10b981'}}>{g.percent_change}%</div>
                      <div style={{fontSize:12,color:'#9fb3c9'}}>{(g.current_close_price||0).toFixed(2)}</div>
                    </div>
                  </div>
                )) : <div style={{color:'#9fb3c9'}}>No data</div>}
              </div>
            </div>
          </aside>
        </section>
      </main>
    </div>
  )
}
