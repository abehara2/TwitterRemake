import React from 'react';
import logo from './logo.svg';
import './App.css';

class App extends React.Component {
	constructor(props) {
		super(props)
		this.state = {
			navam: "uncle",
			arpan: "PM @ MSFT Typescript",
			shreyas: "free t-shirt man"
		}
	}
	randomFunc = () => {
		this.setState({
			navam: "state changed",
		})
	}
	render  () { 
		return (
   			<div className="App">
      			<header className="App-header">
        		<img src={logo} className="App-logo" alt="logo" />
        		<p>
          			Edit <code>src/App.js</code> and save to reload.
        		</p>
        		<a
          		className="App-link"
          		href="https://reactjs.org"
          		target="_blank"
          		rel="noopener noreferrer"
        		>
          			Learn React
        		</a>
				<div>{this.props.val}</div>
				<div>{this.props.key}</div>
				<div>{this.state.shreyas}</div>
				<div>{this.state.navam}</div>
      			</header>
    			</div>
  		);
	}
}
export default App;

