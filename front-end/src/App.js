import React from 'react';

import './App.css';

import QueryBlock from "./QueryBlock";
import ResultBlock from "./ResultBlock";

class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            currentQuery: '',
            ratios: ['1', '1', '1', '1'],
        };
        this.folders = [];

        this.handleQueryChange = this.handleQueryChange.bind(this);
        this.handleRatiosChange = this.handleRatiosChange.bind(this);

        this.getQueriesFolder();
    }

    async getQueriesFolder() {
        const response = await fetch("http://localhost:5000/queries");
        const myJson = await response.json();
        this.folders =  myJson['folders'];
        this.setState({
            currentQuery: myJson['folders'][0]
        });
    }

    handleQueryChange(event) {
        this.setState({
            currentQuery: event.target.id
        });
    }

    handleRatiosChange(event) {
        let name = event.target.name;
        let newRatios = [...this.state.ratios];
        let index;
        if (name === 'color') {
            index = 0;
        } else if (name === 'motion') {
            index = 1;
        } else if (name === 'sound') {
            index = 2;
        } else {
            index = 3;
        }
        newRatios[index] = event.target.value;
        this.setState({ratios: newRatios});
    }

    render() {
        return (
            <div className="App">
                <QueryBlock folders={this.folders}
                            currentQuery={this.state.currentQuery}
                            ratios={this.state.ratios}
                    onQueryChange={this.handleQueryChange} onRatiosChange={this.handleRatiosChange}
                />
                <ResultBlock />
            </div>
        );
    }
}

export default App;
