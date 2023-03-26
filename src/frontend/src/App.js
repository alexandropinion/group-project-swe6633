import logo from './logo.svg';
import './App.css';
import Home from './components/Home';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import { GetRequest } from './GetRequest';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path = '/' element={<Home />} />
        </Routes>
      </Router>
      <h3 className='App'>read-datasets</h3>
      <GetRequest/>
    </div>
  );
}

export default App;
