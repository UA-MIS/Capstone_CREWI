import './App.css';
import './styling/HeaderStyle.css'
import './styling/NavbarStyle.css'
import './styling/LoginStyle.css'
import './styling/WidgetStyle.css'
import './styling/FooterStyle.css'
import MainComponent from './components/MainComponent';
import SocialFollow from "./components/FooterComponent"

function App() {
  return (
    <div className="App">
        <MainComponent/>
    </div>
  );
}

export default App;
