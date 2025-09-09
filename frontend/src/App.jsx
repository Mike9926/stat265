import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './components/Home'
import Market from './pages/Market'
import StockDetail from './pages/StockDetail'

export default function App(){
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home/>} />
        <Route path='/market' element={<Market/>} />
        <Route path='/market/:id' element={<StockDetail/>} />
      </Routes>
    </BrowserRouter>
  )
}
