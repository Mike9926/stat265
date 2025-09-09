import React, {useEffect, useState} from 'react'
import axios from 'axios'
import {useParams} from 'react-router-dom'

export default function StockDetail(){
  const {id} = useParams()
  const [stock,setStock] = useState(null)
  useEffect(()=>{
    axios.get(`/api/stocks/${id}/`).then(r=>setStock(r.data)).catch(()=>{})
  },[id])

  if(!stock) return <div style={{maxWidth:1100,margin:'2rem auto'}}>Loading...</div>

  return (
    <div style={{maxWidth:1100,margin:'2rem auto'}}>
      <h2>{stock.symbol}</h2>
      <div>Price: {stock.current_close_price}</div>
      <div>Change: {stock.percent_change}%</div>
      <h3>Historical (last {stock.historical.length})</h3>
      <div style={{maxHeight:300,overflow:'auto'}}>
        <table style={{width:'100%'}}>
          <thead><tr><th>timestamp</th><th>close</th></tr></thead>
          <tbody>
            {stock.historical.map((h,i)=> (
              <tr key={i}><td>{h.timestamp}</td><td>{h.close_price}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
