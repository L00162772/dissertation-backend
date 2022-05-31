import './App.css';
import Create from './components/create';
import Read from './components/read';
import Update from './components/update';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <Router>
      <div className="main">
        <h2 className="main-header">React User Tracking</h2>
        <div>
        <Routes>
          <Route exact path='/create' element={<Create />} />
          <Route exact path='/read' element={<Read />} />
          <Route path='/update' element={<Update />} />
          <Route exact path='/' element={<Create />} />
          </Routes>
        </div>
        <div style={{ marginTop: 20 }}>
          
        </div>

        
      </div>
    </Router>
  );
}

export default App;
