import React, {useEffect, useState} from 'react'
import axios from 'axios'

export default function Market(){
  const [stocks,setStocks] = useState([])
  useEffect(()=>{
    axios.get('/api/stocks/').then(r=>setStocks(r.data)).catch(()=>{})
  },[])

  return (
    <div style={{maxWidth:1100,margin:'2rem auto'}}>
      <h2 style={{color:'#cfe8ff'}}>Market Data</h2>
      <div style={{background:'#071a2a',padding:12,borderRadius:8}}>
        {stocks.length===0 && <div style={{color:'#9fb3c9'}}>No data</div>}
        {stocks.map(s=> (
          <div key={s.id} style={{display:'flex',justifyContent:'space-between',padding:'10px 6px',borderBottom:'1px solid rgba(255,255,255,0.02)'}}>
            <div style={{fontWeight:600}}>{s.symbol}</div>
            <div style={{textAlign:'right'}}>
              <div style={{color:s.percent_change>=0? '#10b981':'#ef4444'}}>{s.percent_change}%</div>
              <div style={{color:'#9fb3c9'}}>{(s.current_close_price||0).toFixed(2)}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
